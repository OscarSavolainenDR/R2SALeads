from django.shortcuts import render
from rest_framework import generics, status
from ..serializers.project_serializers import ListingSerializer
from ..models import Listing, User, Notification, Attachment, Session, City, Authorised_Listings
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
import json
import pandas as pd
import os
import boto3
import gzip

from .auth_views import authenticate_from_session_key

# import logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
# file_handler = logging.FileHandler(os.path.join(os.getcwd(),'custom_logs','project.log'))
# file_handler.setFormatter(formatter)
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)
# logger.addHandler(file_handler)
# logger.addHandler(stream_handler)


import logging
logger = logging.getLogger(__name__)


def find_indices(lst, condition):
    return [i for i, elem in enumerate(lst) if condition(elem)]


class UpdateScrumBoardBackend(APIView):
    # serializer_class = RoomSerializer
    # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):
        user = authenticate_from_session_key(request)
        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED) 
        
        # Get listing id, where it came from (e.g. leads) and where its going (e.g. contacted)
        listing_id = request.data['draggableId']
        listing_from = request.data['source']['droppableId']
        listing_to = request.data['destination']['droppableId']
        logger.info(f'For user {user.username}, deleting {listing_id} from {listing_from}, adding to {listing_to}')

        # CHnage the listing's status for that user
        user_listing = Authorised_Listings.objects.filter(user=user.profile, listing_id = listing_id)[0]
        if listing_to == 'Leads':
            user_listing.status = 0
        elif listing_to == 'Contacted':
            user_listing.status = 1
        elif listing_to == 'Viewing Booked':
            user_listing.status = 2
        user_listing.save()
        user.save()

        return Response(status=status.HTTP_200_OK)


class DownloadExcel(APIView):
    # serializer_class = RoomSerializer
    # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):

        if 'Authorization' in request.headers:
            user = authenticate_from_session_key(request)
            if user is None:
                return Response(status=status.HTTP_401_UNAUTHORIZED) 
        else:
            user = User.objects.filter(username="Listings_Sample")[0]
        
        logger.info(f'Downloading excel {request.data["file_id"]} for user {user.username}')

        # AWS S3 storage
        BUCKET = os.getenv('AWS_STORAGE_BUCKET_NAME')
        ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
        SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
        s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY) 
        
        # Find listing by id. Only search user's authorised listings.
        listing_query = user.profile.user_listings.filter(id=request.data['file_id'])

        if listing_query.exists():
            listing = listing_query[0]
            city = listing.city.name

            # Stored in DB, tells us what element of JSON array has listing info
            listing_DB_and_JSON_index = int(listing.excel_sheet) 
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            # with gzip.open(os.path.join('listings_json_data','json_data_' + city + '.json'), 'r') as fin:
            #     all_listings = json.loads(fin.read().decode('utf-8'))

            # filename = os.path.join('past_files','listings_json_data','json_data_' + city + '.gz')
            filename = 'past_files/listings_json_data/json_data_' + city + '.gz'
            logger.info(f"Loading listings for excel read: {city} - {filename}")
            obj = s3_resource.Object(BUCKET, filename)
            with gzip.GzipFile(fileobj=obj.get()["Body"]) as gzipfile:
                all_listings = json.loads(gzipfile.read())

        except Exception as e: 
            logger.error(f'Failed to read excel, file {filename}')
            logger.error(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Get listing info from JSON array
        listing = all_listings[listing_DB_and_JSON_index]

        # Remove redundant columns for some rows
        for index, airbnb in enumerate(listing[1:]):
            airbnb.pop('Listing URL', None)
            airbnb.pop('Listing Daily Rent', None)
            airbnb.pop('Listing Bedrooms', None)
            airbnb.pop('Listing Bathrooms', None)
            airbnb.pop('Mean Monthly Income', None)
            airbnb.pop('Median Monthly Income', None)
            
            listing[index+1] = airbnb
        # listing[0]['Listing Monthly Rent'] = listing[0].pop('Listing Daily Rent')*30

        # Move monthly rent to other column in excel (earlier position in dict)
        pos = list(listing[0].keys()).index('Listing Bedrooms')
        items = list(listing[0].items())
        items.insert(pos, ('Listing Monthly Rent', listing[0].pop('Listing Daily Rent')*30))
        listing[0] = dict(items)

        # Move Distances to next to Daily Income, if not already done
        pos = list(listing[0].keys()).index('Mean Monthly Income')
        items = list(listing[0].items())
        distance = listing[0].pop('Distance (km)')
        items.insert(pos, ('Distance (km)', distance))
        listing[0] = dict(items)


        logger.info(f'Successfully downloaded excel {request.data["file_id"]} for user {user.username}')
        return Response({'data': json.dumps(listing)}, status=status.HTTP_200_OK)


class GetTableLeads(APIView):
    # serializer_class = RoomSerializer
    # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):

        if 'Authorization' in request.headers:
            user = authenticate_from_session_key(request)
            if user is None:
                return Response(status=status.HTTP_401_UNAUTHORIZED) 
        else:
            user = User.objects.filter(username="Listings_Sample")[0]

        table_data = request.data['tableData']
        filter_data = request.data['filterData']

        # NOTE: Add a serializer here, very important for query safety
        page_index = table_data['pageIndex']
        page_size = table_data['pageSize']
        sort = table_data['sort']
        query = table_data['query'] 
        order = sort['order']
        search_key = sort['key'] 
        statuses = filter_data['status']

        # import pdb; pdb.set_trace()
        listings = user.profile.user_listings.all()

        total_listings_len = len(listings)
        logger.info(f'User {user.username} has {total_listings_len} listings')

        if query:
            # import pdb; pdb.set_trace()
            listings = (listings.filter(city__name__icontains=query) | listings.filter(city__country__icontains=query) | listings.filter(expected_income__icontains=query) | listings.filter(url__icontains=query)).distinct()

        # NOTE: put as search term in sorting
        logger.info(f'After query {query}, user {user.username} has {len(listings)} listings')
        # Get everything with status not in the filtered data
        not_statuses = []
        for status_ in range(4):
            if status_ not in statuses:
                not_statuses.append(status_)

        # logger.info('User {user.username}, has not statuses', not_statuses)
        for status_ in not_statuses:
            # logger.info('Status', status_)
            listings = listings.exclude(authorised_listings__user=user.profile, authorised_listings__status=status_)

        # logger.info(f'We still have {len(listings)} listings')
        # Sort data (by alphabetical order)
        if search_key:
            if (not search_key == 'status') and (not search_key == 'country'):
                if order == 'desc':
                    listings = listings.order_by(search_key)
                else: 
                    listings = listings.order_by('-' + search_key)
            elif search_key =='status': 
                # import pdb; pdb.set_trace()
                # we want to find all listings the user is subscribed to, and sort the listings by that order
                leads = listings.filter(authorised_listings__user=user.profile, authorised_listings__status=0)
                contacted = listings.filter(authorised_listings__user=user.profile, authorised_listings__status=1)
                booked = listings.filter(authorised_listings__user=user.profile, authorised_listings__status=2)

                if order == 'desc':
                    listings = leads.union(contacted, all=True).union(booked, all=True)
                else:
                    listings = booked.union(contacted, all=True).union(leads, all=True)

            elif search_key == 'country':
                # import pdb; pdb.set_trace()
                for city_nb, city in enumerate(City.objects.filter()):
                    if city_nb == 0:
                        listings_list = listings.filter(city__country=city.country)
                    else:
                        listings_list = listings_list.union(listings.filter(city__country=city.country))
        else:
            listings = listings.order_by('postcode')

        # Bunch into pages, maybe do myself.
        # breakpoint()
        p = Paginator(listings, page_size)
        page_listings = p.page(page_index).object_list

        # Iterate through listings, return only what is needed
        sent_listings = []
        for listing in page_listings:
            l = {
                    'city': listing.city.name,
                    'country': listing.city.country,
                    'postcode': listing.postcode,
                    'bedrooms': listing.bedrooms,
                    'breakeven': listing.breakeven_occupancy,
                    'rent': listing.rent,
                    'expected_income': listing.expected_income,
                    'profit': listing.profit,
                    'status': listing.authorised_listings_set.get(user=user.profile).status,
                    'url': listing.url,
                    'id': listing.id,
                }
            # if l not in sent_listin
            sent_listings.append(l)

        # Serialize response
        # serialized_leads = ListingSerializer(page_listings, many=True).data

        # If no listings, we send them some empty listings encouraging
        # them to subscribe
        if not total_listings_len > 0:
            logger.info(f'No listings found for {user.username}')
            # Dummy listing
            # Iterate through listings, return only what is needed
            sent_listings = []
            l = {
                    'city': 'Subscribe',
                    'country': 'to a City',
                    'postcode': '',
                    'bedrooms': 0,
                    'breakeven' : 0,
                    'rent': 0,
                    'expected_income': 0,
                    'profit': 0,
                    'status': 0,
                    'url': 'to get Leads'
                }
            sent_listings.append(l)
            # print(serialized_q)

            # print(serialized_leads)
            # NOTE: Need to upDATE! WRONG, NEED MISSING DETAILS FOR TABLE
            response_data = {
                'data': json.dumps(sent_listings),
                'total': len(sent_listings),
            }
            # {"msg": f"There are currently no listings in those cities the user {user.username} is authorised to see."}
            return Response(response_data, status=status.HTTP_200_OK)
        
        # print(serialized_leads)
        # Send the response (the listings we have found that match the user's cities and 
        # authorised listing_ids)
        # print(serialized_q) 
        response_data = {
            'data': json.dumps(sent_listings),
            'total': total_listings_len,
            }
        return Response(response_data, status=status.HTTP_200_OK) # Send the listing details to frontend


# class GetScrumBoard(APIView):
#     # serializer_class = RoomSerializer
#     # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

#     # Define a get request: frontend asks for stuff
#     def post(self, request, format=None):

#         user = authenticate_from_session_key(request)
#         if user is None:
#             return Response(status=status.HTTP_401_UNAUTHORIZED) 
        
#         # import pdb; pdb.set_trace()
#         listings = user.profile.user_listings.all()

#         # Create empty querysets
#         listing_queryset_leads = Listing.objects.none()
#         listing_queryset_contacted = Listing.objects.none()
#         listing_queryset_booked = Listing.objects.none()

#         for listing in listings:

#             # Very ugly, but works. Should be a way to access it directly
#             user_listing = Authorised_Listings.objects.filter(listing=listing, user=user.profile)[0]
#             listing_status = user_listing.status

#             # Add to appropriate queryset based on listing status
#             if listing_status == 0:
#                 listing_queryset_leads |= Listing.objects.filter(pk=listing.pk)
#             elif listing_status == 1:
#                 listing_queryset_contacted |= Listing.objects.filter(pk=listing.pk)
#             elif listing_status == 2:
#                 listing_queryset_booked |= Listing.objects.filter(pk=listing.pk)


#         # Serialize responses
#         serialized_leads = ListingSerializer(listing_queryset_leads, many=True).data
#         serialized_contacted = ListingSerializer(listing_queryset_contacted, many=True).data
#         serialized_booked = ListingSerializer(listing_queryset_booked, many=True).data

#         serialized_q = {
#             'Leads': serialized_leads,
#             'Contacted': serialized_contacted,
#             'Viewing Booked': serialized_booked,
#         }

#         # If no listings, we send them some empty listings encouraging
#         # them to subscribe
#         if not ( (len(listing_queryset_leads)>0) or (len(listing_queryset_contacted)>0) or (len(listing_queryset_booked)>0) ):
#             logger.info(f'No listings found for {user.username}')
#             # Dummy listing
#             city = City(name='None')
#             if not City.objects.filter(name='None').exists():
#                 city.save()
#                 city = City.objects.filter(name='None')[0]
#             else:
#                 city = City.objects.filter(name='None')[0]
    
#             temp_queryset = Listing.objects.filter(city=city)
#             if not temp_queryset.exists():
#                 temp_listing = Listing(city=city, name='Subscribe to a city to start receiving R2SA Leads!',
#                                         description='Go to the Manage Lead Subscriptions panel to subscribe to a city.',
#                                         comments = '', labels = ['1k+ profit'],
#                                         rent = 0, profit = 0, expected_income = 0)
#                 attachment =    Attachment.objects.create(name = '', src='', size='',)
#                 attachment.save()
#                 temp_listing.save()
#                 temp_listing.attachments.add(attachment)
#                 # temp_listing.save()
#                 temp_queryset = Listing.objects.filter(city=city)
#             else:
#                 temp_listing = temp_queryset[0]
#                 # attachment = temp

#             serialized_leads = ListingSerializer(temp_queryset, many=True).data
#             serialized_q = {
#                 'Leads': serialized_leads,
#             }
#             temp_listing.delete()
#             attachment.delete()
#             # print(serialized_q)

#             # {"msg": f"There are currently no listings in those cities the user {user.username} is authorised to see."}
#             return Response(serialized_q, status=status.HTTP_200_OK)
        
#         # Send the response (the listings we have found that match the user's cities and 
#         # authorised listing_ids)
#         # print(serialized_q) 
#         return Response(serialized_q, status=status.HTTP_200_OK) # Send the listing details to frontend



class UpdateLeadsListBackend(APIView):
    # serializer_class = RoomSerializer
    # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):
        user = authenticate_from_session_key(request)
        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED) 

        updates = request.data

        for update in updates:

            # Get listing id, where it came from (e.g. leads) and where its going (e.g. contacted)
            listing_id = update['listing_id']
            listing_from = update['status']
            listing_to = (listing_from + 1) % 4 # can be 0, 1, 2, or 3, and toggling cycles them.
            # print(request.data)
            logger.info(f'For user {user.username}, deleting {listing_id} from {listing_from}, adding to {listing_to}')
        
            # Change the listing's status for that user
            user_listing = Authorised_Listings.objects.filter(user=user.profile, listing_id = listing_id)[0]
            user_listing.status = listing_to
            # if listing_to == 0:
            #     user_listing.status = 0
            # elif listing_to == 'Contacted':
            #     user_listing.status = 1
            # elif listing_to == 'Viewing Booked':
            #     user_listing.status = 2
            user_listing.save()
        user.save()

        return Response(status=status.HTTP_200_OK)

