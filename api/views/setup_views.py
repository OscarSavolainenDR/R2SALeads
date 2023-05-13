from django.shortcuts import render
from rest_framework import generics, status
from ..serializers.project_serializers import ListingSerializer
from ..serializers.notification_serializers import  NotificationSerializer
from ..models import Listing, User, Notification, Attachment, City, Subscription
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
import json
from datetime import date, timedelta
import stripe
import os
import numpy as np
import boto3
from django.views.decorators.csrf import csrf_exempt
import zlib 
import gzip

from .auth_views import authenticate_from_session_key
from ..tasks import load_and_store_new_listings_celery, update_listings_for_users_2_celery, financial_logic, update_listings_master_celery
 
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
 
from .cities import cities as cities

# import logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
# file_handler = logging.FileHandler(os.path.join(os.getcwd(),'custom_logs','setup.log'))
# file_handler.setFormatter(formatter)
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)
# logger.addHandler(file_handler)
# logger.addHandler(stream_handler)

import logging
logger = logging.getLogger(__name__)


## Just for filling the DB with dummy data, can be adapted later for actually updating the DB.
class InitDB(APIView):
    """
    Updates cities list, and subscribes admin to all cities.
    """
    today = date.today()
    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):

        # Checks authorisation here, only continues if the code is accepted.
        auth = request.data
        if not 'auth_key' in auth:
            logger.error('No auth key given during InitDB')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            given_auth_key = auth['auth_key']
    
        # Incorrect auth key was given
        if not given_auth_key == os.getenv('UPDATE_DB_AUTH_KEY'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        logger.info('Correct auth key given, running Init DB')

        # Create admin
        if not User.objects.filter(username='admin').exists():
            admin = User(username='admin',
                email = os.getenv('ADMIN_EMAIL'))
            admin.set_password(os.getenv('ADMIN_PASSWORD'))
            admin.save()
            stripe_response = stripe.Customer.create(
                email = admin.email,
                name = admin.username
            )
            # admin.profile.authorisations = ['user'],
            admin.profile.stripe_customer_id = stripe_response.id
            admin.save()
        else:
            admin = User.objects.filter(username='admin')[0]
            admin.email = os.getenv('ADMIN_EMAIL')
            admin.set_password(os.getenv('ADMIN_PASSWORD'))
            admin.save()

        # Get all cities currently in DB
        cities_in_DB = City.objects.all()
        # cities_in_DB_names = [city.name for city in cities_in_DB]

        city_names = []
        for city in cities:
            if type(city) is tuple:
                city = city[0]

            # Get all cities in provided variable
            city_names.append(city['name'])

        # Delete cities in DB that aren't in the provided cities variable
        for city_in_DB in cities_in_DB:
            if city_in_DB.name not in city_names:
                logger.debug(f"{city_in_DB.name} deleted from DB")
                city_in_DB.delete()

        for city in cities:
            if type(city) is tuple:
                city = city[0]

            # If new, create.
            city_query = City.objects.filter(name=city['name'])
            if not city_query.exists():
                city_elem = City(name=city['name'], country=city['country'], price=city['price'], stripe_subscription_code=city['stripe_subscription_code'])
                city_elem.save()
            # If already exists, just update the city (since pricing may change).
            else:
                logger.info(f"Updating city {city['name']}")
                city_elem = city_query[0]
                city_elem.price = city['price']
                city_elem.country = city['country']
                city_elem.stripe_subscription_code = city['stripe_subscription_code']
                city_elem.save()

            # Subscribe admin to all cities
            admin.profile.cities.add(city_elem)

        update_listings_for_users_2_celery()

        return Response(status=status.HTTP_200_OK)
  

class UpdateListings(APIView):
    @csrf_exempt
    def post(self, request, format=None):
        """
        Expects one city to be updated, and for the city_name to be sent over API.
        It will read the listings data from AWS S3 bucket.
        """

        # Decompresses data
        body = json.loads(request.body)

        # Checks authorisation here, only continues if the code is accepted.
        if not 'auth_key' in body:
            logger.error('No auth key given during UpdateListings')  
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            given_auth_key = body['auth_key']
    
        # Incorrect auth key was given
        if not given_auth_key == os.getenv('UPDATE_DB_AUTH_KEY'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

        # if not 'data' in body or not 'listings' in body['data']:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # listings = body['data']['listings']
        city_name = body['city']

        logger.info(f'Correct auth key given, running UpdateListings for {city_name}')

        # # Save communicated listings to json file, a bit slow but good to have them.
        # # We could probably just save the original communicated compressed data.
        # json_bytes = json.dumps(listings).encode('utf-8') # bytes
        # save_file = os.path.join("listings_json_data",f"json_data_{city_name}.json") 

        load_and_store_new_listings_celery.delay(city_name)

        update_listings_for_users_2_celery()

        return Response(status=status.HTTP_200_OK)


class UpdateListingsWithInPlaceFiles(APIView):
    """
    Same as UpdateLisitngs, but we don't give it any new data.
    We just update the listings with the current files. Mainly used for debugging.
    """
    def post(self, request, format=None):

        # Checks authorisation here, only continues if the code is accepted.
        auth = request.data
        if not 'auth_key' in auth:
            logger.error('No auth key given during UpdateListingsWithInPlaceFiles')  
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            given_auth_key = auth['auth_key']
    
        # Incorrect auth key was given
        if not given_auth_key == os.getenv('UPDATE_DB_AUTH_KEY'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        logger.info('Correct auth key given, running UpdateListingsWithInPlaceFiles')

        update_listings_master_celery()

        return Response(status=status.HTTP_200_OK)

class WipeListings(APIView):
    """
    We delete all listings from DB, used for debugging. NOTE: THIS SHOULD BE DELETED IN PRODUCTION, TOO DANGEROUS.
    """
    def post(self, request, format=None):

        # Checks authorisation here, only continues if the code is accepted.
        auth = request.data
        if not 'auth_key' in auth:
            logger.error('No auth key given during WipeListings')  
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            given_auth_key = auth['auth_key']
    
        # Incorrect auth key was given
        if not given_auth_key == os.getenv('UPDATE_DB_AUTH_KEY'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        logger.info('Correct auth key given, running WipeListings')

        Listing.objects.all().delete()

        return Response(status=status.HTTP_200_OK)