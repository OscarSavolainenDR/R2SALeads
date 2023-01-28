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
            print(key)

            # Load user's details from DB
            # username = 'Tim' # request.session['username']
            queryset = User.objects.filter(username=username)
            if queryset.exists():
                user = queryset[0]
                print(f'User {user.username} found!')
            else:
                return Response({'msg': f'User {username} not a valid user'}, status=status.HTTP_401_UNAUTHORIZED) 

            # NOTE: add serializer

            # Find all listings in the given user's cities
            # Leads
            my_filter_qs = Q()
            no_listings = True
            for city in user.profile.cities.all():
                # Get only the listings they have the IDs for
                for listing_id in user.profile.authorised_listings_leads:  
                    my_filter_qs = my_filter_qs | (Q(id=listing_id) & Q(city=city))
                    no_listings = False
            if no_listings:
                listing_queryset_leads = []
            else:
                listing_queryset_leads = Listing.objects.filter(my_filter_qs)

            # Contacted
            my_filter_qs = Q()
            no_listings = True
            for city in user.profile.cities.all():
                # Get only the listings they have the IDs for
                for listing_id in user.profile.authorised_listings_contacted:  
                    my_filter_qs = my_filter_qs | (Q(id=listing_id) & Q(city=city))
                    no_listings = False
            if no_listings:
                listing_queryset_contacted = []
            else:
                listing_queryset_contacted = Listing.objects.filter(my_filter_qs)
            # print('Contacted:', user.authorised_listings_contacted)

            # Viewing booked
            my_filter_qs = Q()
            no_listings = True
            for city in user.profile.cities.all():
                # Get only the listings they have the IDs for
                for listing_id in user.profile.authorised_listings_booked:  
                    my_filter_qs = my_filter_qs | (Q(id=listing_id) & Q(city=city))
                    no_listings = False
            if no_listings:
                listing_queryset_booked = []
            else:
                listing_queryset_booked = Listing.objects.filter(my_filter_qs)

            # Serialize responses
            # serialized_leads = []
        # if listing_queryset_leads.exists():
            serialized_leads = ListingSerializer(listing_queryset_leads, many=True).data

            # serialized_contacted = []
            # if listing_queryset_contacted.exists():
            serialized_contacted = ListingSerializer(listing_queryset_contacted, many=True).data

            # serialized_booked = []
            # if listing_queryset_booked.exists():
            serialized_booked = ListingSerializer(listing_queryset_booked, many=True).data

            # print('Serialized booked', serialized_booked)

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
                                            comments = '', labels = ['1k+ profit'],)
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
    def get(self, request, format=None):
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

            print(request)

            excel_path = 'excels/Bristol.xlsx'
            listing_sheet = 'Listing_3'

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
            print(key)

            # Load user's details from DB
            # username = 'Tim' # request.session['username']
            queryset = User.objects.filter(username=username)
            if queryset.exists():
                user = queryset[0]
                print(f'User {user.username} found!')
            else:
                return Response({'msg': f'User {username} not a valid user'}, status=status.HTTP_401_UNAUTHORIZED) 


            # NOTE: Add a serializer here, very important for query safety
            page_index = request.data['pageIndex']
            page_size = request.data['pageSize']
            sort = request.data['sort']
            query = request.data['query']
            order = sort['order']
            search_key = sort['key']

            # import pdb; pdb.set_trace()
            listings = user.profile.user_listings.all()

            print('Query =', query)
            if query:
                listings = (listings.filter(name__icontains=query) | listings.filter(country__icontains=query) | listings.filter(expected_income__icontains=query)).distinct()
            # NOTE: put as search term in sorting

            # Sort data (by alphabetical order)
            if search_key:
                if not search_key == 'status':
                    if order == 'desc':
                        listings = listings.order_by(search_key)
                    else: 
                        listings = listings.order_by('-' + search_key)
                else: 
                    # import pdb; pdb.set_trace()
                    # we want to find all listings the user is subscribed to, and sort the listings by that order
                    subscribed = user.profile.listings.all()
                    all_not_subscribed = City.objects.exclude(pk__in=subscribed.values_list('pk', flat=True))
                    all_not_subscribed = all_not_subscribed.exclude(name='None')

                    if order == 'desc':
                        listings = subscribed.union(all_not_subscribed, all=True) 
                    else:
                        listings = all_not_subscribed.union(subscribed, all=True)

            # Bunch into pages, maybe do myself.
            p = Paginator(listings, page_size)
            page_listings = p.page(page_index).object_list

            # Serialize response
            serialized_leads = ListingSerializer(page_listings, many=True).data

            # If no listings, we send them some empty listings encouraging
            # them to subscribe
            if not len(listings) > 0:
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
                                            comments = '', labels = ['1k+ profit'],)
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
                temp_listing.delete()
                attachment.delete()
                # print(serialized_q)

                # {"msg": f"There are currently no listings in those cities the user {user.username} is authorised to see."}
                return Response(serialized_leads, status=status.HTTP_200_OK)
            
            # Send the response (the listings we have found that match the user's cities and 
            # authorised listing_ids)
            # print(serialized_q) 
            return Response(serialized_leads, status=status.HTTP_200_OK) # Send the listing details to frontend
        return Response({'msg': 'Session not found.'}, status=status.HTTP_401_UNAUTHORIZED)


class GetScrumBoard_2(APIView):
    # serializer_class = RoomSerializer
    # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):

        key = request.headers['Authorization'].split(' ')[1]
        # Have a Serializer HERE!
        key_query_set = Session.objects.filter(key=key)

        if key_query_set.exists():
            username = key_query_set[0].username
            print(key)

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
                                            comments = '', labels = ['1k+ profit'],)
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

