from django.shortcuts import render
from rest_framework import generics, status
from ..serializers.subscription_serializers import ReturnBasketSerializer, SubscriptionSerializer,  UnsubscribeSerializer, AddToBasketSerializer, GetBasketSerializer,CheckoutBasketSerializer
from ..serializers.auth_serializers import SessionSerializer
from ..models import Listing, User, Notification, Attachment, Session, City
from rest_framework.views import APIView 
from rest_framework.response import Response 
from django.http import JsonResponse
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator
import json
from datetime import date

class GetSubscriptionOptions(APIView):
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
            key = sort['key']

            cities = City.objects.exclude(name='None') # all cities

            print('Query =', query)
            if query:
                cities = (cities.filter(name__icontains=query) | cities.filter(country__icontains=query) | cities.filter(price__icontains=query)).distinct()
            # NOTE: put as search term in sorting

            # Sort data (by alphabetical order)
            if order == 'desc':
                cities = cities.order_by('name')
            else:
                cities = cities.order_by('-name')

            # Bunch into pages, maybe do myself.
            p = Paginator(cities, page_size)
            page_cities = p.page(page_index).object_list

            # city_subscription_statuses = []
            data = [] # What we JSONify and send out
            for city in page_cities:
                # Check if city is in user subscriptions
                # city.user_set.all()
                if user.profile.cities.filter(name=city.name).exists():
                    subscribed = 0
                elif user.profile.cities_basket.filter(name=city.name).exists():
                    subscribed = 1
                    # city_subscription_statuses.append([city.id, 0]) # subscribed
                else:
                    subscribed = 2
                    # city_subscription_statuses.append([city.id, 2]) # not subscribed

                city_info = {
                    'id': city.id,
                    'name': city.name,
                    'country': city.country,
                    'status': subscribed,
                    'price': city.price,
                    'description': city.description,
                }
                data.append(city_info)

            total_len = len(cities)
            # page_cities = SubscriptionSerializer(page_cities, many=True).data
            response_data = {
                'data': json.dumps(data),
                'total': total_len,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        return Response({'msg': 'Session data not valid.'}, status=status.HTTP_401_UNAUTHORIZED)
         

class UnsubscribeFromCity(APIView):
    serializer_class = UnsubscribeSerializer
    # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):

        key = request.headers['Authorization'].split(' ')[1]
        key_query_set = Session.objects.filter(key=key)

        if key_query_set.exists():
            username = key_query_set[0].username
            print(key)

            queryset = User.objects.filter(username=username)
            if queryset.exists():
                user = queryset[0]
                print(f'User {user.username} found!')
            else:
                return Response({'msg': f'User {username} not a valid user'}, status=status.HTTP_401_UNAUTHORIZED) 

            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                id = request.data['id']
                city_name = request.data['name']
                print(f'Unsubscribe city {city_name} id is {id}')
                city_query = City.objects.filter(name=city_name)

                if city_query.exists():
                    city = city_query[0] 

                    # If in subscripted to cities
                    if user.profile.cities.filter(name=city.name).exists():
                        user.profile.cities.remove(city)

                    # If city merely in checkout basket
                    if user.profile.cities_basket.filter(name=city.name).exists():
                        user.profile.cities_basket.remove(city)
                    user.profile.save()

                print('Successfully unsubscribed')
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': 'Session data not valid.'}, status=status.HTTP_401_UNAUTHORIZED)
         

class AddCitytoBasket(APIView):
    serializer_class = AddToBasketSerializer
    # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):

        key = request.headers['Authorization'].split(' ')[1]
        # Have a Serializer HERE!
        # serializer = SessionSerializer(data=key)
        # print(key, serializer)
        # if serializer.is_valid():

        # key = request.headers['Authorization'].split(' ')[1]
        key_query_set = Session.objects.filter(key=key)

        if key_query_set.exists():
            username = key_query_set[0].username
            print(key)

            queryset = User.objects.filter(username=username)
            if queryset.exists():
                user = queryset[0]
                print(f'User {user.username} found!')
            else:
                return Response({'msg': f'User {username} not a valid user'}, status=status.HTTP_401_UNAUTHORIZED) 

            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(): # check if data in our post request is valid

                id = request.data['id']
                city_name = request.data['name']
                print(f'Add city {city_name} to basket, id is {id}')
                city_query = City.objects.filter(name=city_name)

                if city_query.exists():
                    city = city_query[0] 

                # If already subscribed
                if user.profile.cities.filter(name=city.name).exists():
                    return Response({'message': f'User ({username}) is already subscribed to that city ({city.name}).'}, status=status.HTTP_400_BAD_REQUEST)

                # # If already subscribed
                # if user.cities_basket.filter(name=city.name).exists():
                #     return Response({'message': f'City ({city.name}) already in basket.'}, status=status.HTTP_400_BAD_REQUEST)

                user.profile.cities_basket.add(city)
                user.save()

                print('Added city to basket')
                return Response(status=status.HTTP_200_OK)
            # print('didnt pass 2nd serialzier')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': 'Session data not valid.'}, status=status.HTTP_401_UNAUTHORIZED)
        # print('didnt pass serializer')
        # return Response(status=status.HTTP_400_BAD_REQUEST)

class GetBasket(APIView):
    serializer_class = CheckoutBasketSerializer
    # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):

        key = request.headers['Authorization'].split(' ')[1]
        key_query_set = Session.objects.filter(key=key)

        if key_query_set.exists():
            username = key_query_set[0].username
            print(key)

            queryset = User.objects.filter(username=username)
            if queryset.exists():
                user = queryset[0]
                print(f'User {user.username} found!')
            else:
                return Response({'msg': f'User {username} not a valid user'}, status=status.HTTP_401_UNAUTHORIZED) 


            cities = user.profile.cities_basket.exclude(name='None') # all cities in basket
            subTotal = 0
            for city in cities:
                # print(city)
                subTotal += city.price
            tax = 0
            total = subTotal + tax

            # page_cities = SubscriptionSerializer(page_cities, many=True).data
            response_data = {
                'product': CheckoutBasketSerializer(cities, many=True).data,
                'paymentSummary': {
                    'subTotal': subTotal,
                    'tax': tax,
                    'total': total,
                },
            }

            return Response(response_data, status=status.HTTP_200_OK)
        return Response({'msg': 'Session data not valid.'}, status=status.HTTP_401_UNAUTHORIZED)
         

# Need to take in data from Stripe
# class SubscribeToCity(APIView):
#     # serializer_class = CheckoutBasketSerializer
#     # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

#     # Define a get request: frontend asks for stuff
#     def post(self, request, format=None):

#         key = request.headers['Authorization'].split(' ')[1]
#         key_query_set = Session.objects.filter(key=key)

#         if key_query_set.exists():
#             username = key_query_set[0].username
#             print(key)

#             queryset = User.objects.filter(username=username)
#             if queryset.exists():
#                 user = queryset[0]
#                 print(f'User {user.username} found!')
#             else:
#                 return Response({'msg': f'User {username} not a valid user'}, status=status.HTTP_401_UNAUTHORIZED) 

#             # Get checkout basket results

#             # Set date they got their first subscription
#             # user.trial_week_start = date.today()
#             # user.trial_city = 

#             # After a 
#             return Response(status=status.HTTP_200_OK)
#         return Response({'msg': 'Session data not valid.'}, status=status.HTTP_401_UNAUTHORIZED)
         
# class Bill(APIView):