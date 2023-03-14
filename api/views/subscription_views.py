from django.shortcuts import render, redirect
from rest_framework import generics, status
from ..serializers.subscription_serializers import ReturnBasketSerializer, SubscriptionSerializer,  UnsubscribeSerializer, AddToBasketSerializer, GetBasketSerializer,CheckoutBasketSerializer
from ..serializers.auth_serializers import SessionSerializer
from ..models import Listing, User, Notification, Attachment, Session, City, Subscription, Authorised_Listings
from rest_framework.views import APIView 
from rest_framework.response import Response 
from django.http import JsonResponse
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator
import json
from datetime import date
import os
import stripe

from .auth_views import authenticate_from_session_key

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
file_handler = logging.FileHandler(os.path.join('logs','subscriptions.log'))
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

class GetSubscriptionOptions(APIView):
    # serializer_class = RoomSerializer
    # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):

        user = authenticate_from_session_key(request)
        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED) 

        # NOTE: Add a serializer here, very important for query safety
        page_index = request.data['pageIndex']
        page_size = request.data['pageSize']
        sort = request.data['sort']
        query = request.data['query']
        order = sort['order']
        search_key = sort['key']

        cities = City.objects.exclude(name='None') # all cities
        total_len = len(cities)

        if query:
            cities = (cities.filter(name__icontains=query) | cities.filter(country__icontains=query) | cities.filter(price__icontains=query)).distinct()
        # NOTE: put as search term in sorting

        # Sort data (by alphabetical order)
        if search_key:
            if not search_key == 'status':
                if order == 'desc':
                    cities = cities.order_by(search_key)
                else: 
                    cities = cities.order_by('-' + search_key)
            else: 
                # import pdb; pdb.set_trace()
                # we want to find all cities the user is subscribed to, and sort the cities by that order
                subscribed = user.profile.cities.all()
                all_not_subscribed = City.objects.exclude(pk__in=subscribed.values_list('pk', flat=True))
                all_not_subscribed = all_not_subscribed.exclude(name='None')

                if order == 'desc':
                    cities = subscribed.union(all_not_subscribed, all=True) 
                else:
                    cities = all_not_subscribed.union(subscribed, all=True) 
                    

        # Bunch into pages, maybe do myself.
        p = Paginator(cities, page_size)
        page_cities = p.page(page_index).object_list

        data = [] # What we JSONify and send out
        for city in page_cities:
            # Check if city is in user subscriptions
            if user.profile.cities.filter(name=city.name).exists():
                subscribed = 0  # subscribed
            elif user.profile.cities_basket.filter(name=city.name).exists():
                subscribed = 1
            else:
                subscribed = 2

            city_info = {
                'id': city.id,
                'name': city.name,
                'country': city.country,
                'status': subscribed,
                'price': city.price,
                'description': city.description,
            }
            data.append(city_info)

        response_data = {
            'data': json.dumps(data),
            'total': total_len,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class UnsubscribeFromCity(APIView):
    serializer_class = UnsubscribeSerializer

    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):

        user = authenticate_from_session_key(request)
        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED) 
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            id = request.data['id']
            city_name = request.data['name']
            logger.info(f'Unsubscribing {user.username} from city {city_name}; city id: {id}')
            city_query = City.objects.filter(name=city_name)

            if city_query.exists():
                city = city_query[0] 

                # If in subscripted-to-cities
                subscription_query = Subscription.objects.filter(city=city, user=user.profile)
                if subscription_query.exists():
                    subscription = subscription_query[0]

                    logger.info(f'Deleting stripe subscription for user {user.username} and city {city.name}')
                    try:
                        response = stripe.SubscriptionItem.delete(
                            subscription.stripe_subscription_id,
                        )
                    except Exception as e:
                        response = stripe.SubscriptionItem.retrieve(
                            subscription.stripe_subscription_id,
                        )
                        response = stripe.Subscription.delete(
                            response.subscription,
                        )
                        
                    # breakpoint()
                    logger.info(f'Deleting subscription from DB for user {user.username} and city {city.name}')
                    user.profile.cities.remove(city)

                    # user_listings = user.profile.user_listings.all()
                    logger.info(f'Removing listings for user {user.username} and city {city.name}')
                    user_listings = Authorised_Listings.objects.filter(listing__city=city, user=user.profile)
                    user_listings.delete()

                # If city merely in checkout basket
                if user.profile.cities_basket.filter(name=city.name).exists(): 
                    user.profile.cities_basket.remove(city)
                user.profile.save()

            logger.info(f'Successfully unsubscribed user {user.username} from city {city.name}')
            return Response(status=status.HTTP_200_OK)
        logger.error('Serializer was not valid')
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AddCitytoBasket(APIView):
    serializer_class = AddToBasketSerializer
    # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):

        user = authenticate_from_session_key(request)
        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED) 
    
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(): # check if data in our post request is valid

            id = request.data['id']
            city_name = request.data['name']
            city_query = City.objects.filter(name=city_name)

            logger.info(f"Adding {city_name} to user {user.username}'s basket")

            if city_query.exists():
                city = city_query[0] 

            # If already subscribed
            if user.profile.cities.filter(name=city.name).exists():
                logger.ingo('User {user.username} already subscribed to {city_name}')
                return Response({'message': f'User ({user.username}) is already subscribed to that city ({city.name}).'}, status=status.HTTP_400_BAD_REQUEST)

            # # If already subscribed
            # if user.cities_basket.filter(name=city.name).exists():
            #     return Response({'message': f'City ({city.name}) already in basket.'}, status=status.HTTP_400_BAD_REQUEST)

            user.profile.cities_basket.add(city)
            user.save()

            logger.info(f"Successfully added {city_name} to user {user.username}'s basket")
            return Response(status=status.HTTP_200_OK)
        # print('didnt pass 2nd serialzier')
        logger.error('Serializer was not valid', request.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GetBasket(APIView):
    serializer_class = CheckoutBasketSerializer
    # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):

        user = authenticate_from_session_key(request)
        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED) 

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

class CheckoutBasket(APIView):
    serializer_class = CheckoutBasketSerializer
    # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):

        user = authenticate_from_session_key(request)
        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED) 
    
        cities = user.profile.cities_basket.exclude(name='None') # all cities in basket
        city_names = [city.name for city in cities]
        logger.info(f'Checking out basket [{city_names}] for {user.username}')
        items = []
        for city in cities:
            items.append(
                {
                    "price": city.stripe_subscription_code,
                    "quantity": 1,
                }
            )

        return Response(json.dumps({'items': items, 'email': user.email}), status=status.HTTP_200_OK)


