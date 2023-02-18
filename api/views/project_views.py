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


def find_indices(lst, condition):
    return [i for i, elem in enumerate(lst) if condition(elem)]

class GetScrumBoardMembers(APIView):
    # serializer_class = RoomSerializer
    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):
        return Response({"msg": f"Something happening ' scrum board members."}, status=status.HTTP_200_OK)


class UpdateScrumBoardBackend(APIView):
    # serializer_class = RoomSerializer
    # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):
        key = request.headers['Authorization'].split(' ')[1]
        key_query_set = Session.objects.filter(key=key)

        if key_query_set.exists():
            username = key_query_set[0].username

            # Load user's details from DB
            queryset = User.objects.filter(username=username)
            if queryset.exists():
                user = queryset[0]
                print(f'User {user.username} found!')
            else:
                return Response({'msg': f'User {username} not a valid user'}, status=status.HTTP_401_UNAUTHORIZED) 

            # Get listing id, where it came from (e.g. leads) and where its going (e.g. contacted)
            listing_id = request.data['draggableId']
            listing_from = request.data['source']['droppableId']
            listing_to = request.data['destination']['droppableId']
            print(f'Deleting {listing_id} from {listing_from}, adding to {listing_to}')

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
        return Response({'msg': 'Session not found.'}, status=status.HTTP_401_UNAUTHORIZED)


class DownloadExcel(APIView):
    # serializer_class = RoomSerializer
    # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):
        key = request.headers['Authorization'].split(' ')[1]
        key_query_set = Session.objects.filter(key=key)

        if key_query_set.exists():
            username = key_query_set[0].username

            # Load user's details from DB
            queryset = User.objects.filter(username=username)
            if queryset.exists():
                user = queryset[0]
                print(f'User {user.username} found!')
            else:
                return Response({'msg': f'User {username} not a valid user'}, status=status.HTTP_401_UNAUTHORIZED) 

            # Find listing by id. Only search user's authorised listings.
            listing_query = user.profile.user_listings.filter(id=request.data['file_id'])

            if listing_query.exists():
                listing = listing_query[0]
                city = listing.city.name

                excel_path = f'excels/{city}.xlsx'
                listing_sheet = f'Listing_{listing.excel_sheet}'
                # breakpoint()
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)


            # try:
            df = pd.read_excel(excel_path, sheet_name=listing_sheet)  # 

            # Initialize data
            data=[0 for i in range(len(df))]
            excel_json_str = []
            for i in range(len(df)):    
                data[i] = { str(df.columns.values[0]): str(df.loc[i][0]), 
                            str(df.columns.values[1]): str(df.loc[i][1]), 
                            str(df.columns.values[2]): str(df.loc[i][2]),
                            str(df.columns.values[3]): str(df.loc[i][3]),
                            str(df.columns.values[4]): str(df.loc[i][4]),
                            str(df.columns.values[5]): str(df.loc[i][5]), 
                            str(df.columns.values[6]): str(df.loc[i][6]), 
                            str(df.columns.values[7]): str(df.loc[i][7]), 
                            str(df.columns.values[8]): str(df.loc[i][8]), 
                            str(df.columns.values[9]): str(df.loc[i][9]), 
                            str(df.columns.values[10]): str(df.loc[i][10]), 
                            str(df.columns.values[11]): str(df.loc[i][11]), 
                            str(df.columns.values[12]): str(df.loc[i][12]), 
                            }
                excel_json_str.append(data[i])
            return Response({'data': json.dumps(excel_json_str)}, status=status.HTTP_200_OK)
        return Response({'msg': 'Session not found.'}, status=status.HTTP_401_UNAUTHORIZED)


class GetTableLeads(APIView):
    # serializer_class = RoomSerializer
    # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):

        key = request.headers['Authorization'].split(' ')[1]
        key_query_set = Session.objects.filter(key=key)

        if key_query_set.exists():
            username = key_query_set[0].username

            # Load user's details from DB
            # username = 'Tim' # request.session['username']
            queryset = User.objects.filter(username=username)
            if queryset.exists():
                user = queryset[0]
                print(f'User {user.username} found!')
            else:
                return Response({'msg': f'User {username} not a valid user'}, status=status.HTTP_401_UNAUTHORIZED) 
            
            print(request.data)

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
            print(f'We start with {len(listings)} listings')
            total_listings_len = len(listings)

            if query:
                # import pdb; pdb.set_trace()
                listings = (listings.filter(city__name__icontains=query) | listings.filter(city__country__icontains=query) | listings.filter(expected_income__icontains=query) | listings.filter(url__icontains=query)).distinct()

            # NOTE: put as search term in sorting
            print(f'We have {len(listings)} listings')
            # Get everything with status not in the filtered data
            not_statuses = []
            for status_ in range(4):
                if status_ not in statuses:
                    not_statuses.append(status_)

            print('Not statuses', not_statuses)
            for status_ in not_statuses:
                print('Status', status_)
                listings = listings.exclude(authorised_listings__user=user.profile, authorised_listings__status=status_)

            print(f'We still have {len(listings)} listings')
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
                if listing.profit < 500:
                    continue
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
                sent_listings.append(l)

            # Serialize response
            # serialized_leads = ListingSerializer(page_listings, many=True).data

            # If no listings, we send them some empty listings encouraging
            # them to subscribe
            if not len(listings) > 0:
                print('No listings found!')
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

                print('We send a response')

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
        return Response({'msg': 'Session not found.'}, status=status.HTTP_401_UNAUTHORIZED)


class GetScrumBoard(APIView):
    # serializer_class = RoomSerializer
    # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):

        key = request.headers['Authorization'].split(' ')[1]
        # Have a Serializer HERE!
        key_query_set = Session.objects.filter(key=key)

        if key_query_set.exists():
            username = key_query_set[0].username

            # Load user's details from DB
            # username = 'Tim' # request.session['username']
            queryset = User.objects.filter(username=username)
            if queryset.exists():
                user = queryset[0]
                print(f'User {user.username} found!')
            else:
                return Response({'msg': f'User {username} not a valid user'}, status=status.HTTP_401_UNAUTHORIZED) 

            # import pdb; pdb.set_trace()
            listings = user.profile.user_listings.all()

            # Create empty querysets
            listing_queryset_leads = Listing.objects.none()
            listing_queryset_contacted = Listing.objects.none()
            listing_queryset_booked = Listing.objects.none()

            for listing in listings:

                # Very ugly, but works. Should be a way to access it directly
                user_listing = Authorised_Listings.objects.filter(listing=listing, user=user.profile)[0]
                listing_status = user_listing.status

                # Add to appropriate queryset based on listing status
                if listing_status == 0:
                    listing_queryset_leads |= Listing.objects.filter(pk=listing.pk)
                elif listing_status == 1:
                    listing_queryset_contacted |= Listing.objects.filter(pk=listing.pk)
                elif listing_status == 2:
                    listing_queryset_booked |= Listing.objects.filter(pk=listing.pk)


            # Serialize responses
            serialized_leads = ListingSerializer(listing_queryset_leads, many=True).data
            serialized_contacted = ListingSerializer(listing_queryset_contacted, many=True).data
            serialized_booked = ListingSerializer(listing_queryset_booked, many=True).data

            serialized_q = {
                'Leads': serialized_leads,
                'Contacted': serialized_contacted,
                'Viewing Booked': serialized_booked,
            }

            # If no listings, we send them some empty listings encouraging
            # them to subscribe
            if not ( (len(listing_queryset_leads)>0) or (len(listing_queryset_contacted)>0) or (len(listing_queryset_booked)>0) ):
                print('No listings found!')
                # Dummy listing
                city = City(name='None')
                if not City.objects.filter(name='None').exists():
                    city.save()
                    city = City.objects.filter(name='None')[0]
                else:
                    city = City.objects.filter(name='None')[0]
        
                temp_queryset = Listing.objects.filter(city=city)
                if not temp_queryset.exists():
                    temp_listing = Listing(city=city, name='Subscribe to a city to start receiving R2SA Leads!',
                                            description='Go to the Manage Lead Subscriptions panel to subscribe to a city.',
                                            comments = '', labels = ['1k+ profit'],
                                            rent = 0, profit = 0, expected_income = 0)
                    attachment =    Attachment.objects.create(name = '', src='', size='',)
                    attachment.save()
                    temp_listing.save()
                    temp_listing.attachments.add(attachment)
                    # temp_listing.save()
                    temp_queryset = Listing.objects.filter(city=city)
                else:
                    temp_listing = temp_queryset[0]
                    # attachment = temp

                serialized_leads = ListingSerializer(temp_queryset, many=True).data
                serialized_q = {
                    'Leads': serialized_leads,
                }
                temp_listing.delete()
                attachment.delete()
                # print(serialized_q)

                # {"msg": f"There are currently no listings in those cities the user {user.username} is authorised to see."}
                return Response(serialized_q, status=status.HTTP_200_OK)
            
            # Send the response (the listings we have found that match the user's cities and 
            # authorised listing_ids)
            # print(serialized_q) 
            return Response(serialized_q, status=status.HTTP_200_OK) # Send the listing details to frontend
        return Response({'msg': 'Session not found.'}, status=status.HTTP_401_UNAUTHORIZED)



class UpdateLeadsListBackend(APIView):
    # serializer_class = RoomSerializer
    # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):
        key = request.headers['Authorization'].split(' ')[1]
        key_query_set = Session.objects.filter(key=key)

        if key_query_set.exists():
            username = key_query_set[0].username

            # Load user's details from DB
            queryset = User.objects.filter(username=username)
            if queryset.exists():
                user = queryset[0]
                print(f'User {user.username} found!')
            else:
                return Response({'msg': f'User {username} not a valid user'}, status=status.HTTP_401_UNAUTHORIZED) 

            print(request.data)
            updates = request.data

            for update in updates:

                # Get listing id, where it came from (e.g. leads) and where its going (e.g. contacted)
                listing_id = update['listing_id']
                listing_from = update['status']
                listing_to = (listing_from + 1) % 4 # can be 0, 1, 2, or 3, and toggling cycles them.
                # print(request.data)
                print(f'Deleting {listing_id} from {listing_from}, adding to {listing_to}')
            
                # CHnage the listing's status for that user
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
        return Response({'msg': 'Session not found.'}, status=status.HTTP_401_UNAUTHORIZED)

