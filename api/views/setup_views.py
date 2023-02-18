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

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

from .cities import test_cities as cities


## Just for filling the DB with dummy data, can be adapted later for actually updating the DB.
class InitDB(APIView):
    today = date.today()
    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):

        # NOTE: Add authorisation here, only if code is accepted.

        for city in cities:
            if type(city) is tuple:
                city = city[0]

            if not City.objects.filter(name=city['name']).exists():
                city_elem = City(name=city['name'], country=city['country'], price=city['price'], stripe_subscription_code=city['stripe_subscription_code'])
                city_elem.save()
      
        if not User.objects.filter(username='admin').exists():
            admin = User(username='admin', password='abc',
                email = 'admin@hotmail.com')
            admin.save()
            stripe_response = stripe.Customer.create(
                email = admin.email,
                name = admin.username
            )
            # admin.profile.authorisations = ['user'],
            admin.profile.stripe_customer_id = stripe_response.id
            admin.save()

        # Notifications

        # # Check if database already has these, if so skip
        # notification_queryset = Notification.objects.filter(userName='Tim')
        # if not notification_queryset.exists():
        #     for i in range(3):
        #         notification = Notification(userName='Tim', description=f'test_{i}')
        #         notification.save()
            
        return Response(status=status.HTTP_200_OK)
  
from django.views.decorators.csrf import csrf_exempt
class UpdateListings(APIView):
    today = date.today()
    @csrf_exempt
    def post(self, request, format=None):

        # Make sure only requests with the code get through
        # if request.data['code'] == 'update':
        #     pass
            
        # load_and_store_new_listings('London')
        for city in cities:
            if type(city) is tuple:
                city = city[0]
            load_and_store_new_listings(city['name'], self.today)

        # Add new listings to Users
        print('Adding new listings to users')
        for listing in Listing.objects.filter():
            # Runs once a day, should catch all new ones.
            # Although more robust to go through all listings
            if listing.created_at <= self.today:
                # print('Listing:', listing.url, listing.id)
                for user in User.objects.filter(): 
                    if user.profile.cities.filter(name=listing.city.name).exists():
                        print(f'Adding listings to {user.username} leads list')
                        if listing not in user.profile.user_listings.all():
                            # NOTE: need to set listing status to 0 for that user.
                            user.profile.user_listings.add(listing)
                        # if listing.id not in user.profile.authorised_listings_leads:
                        #     if listing.id not in user.profile.authorised_listings_contacted:
                        #         if listing.id not in user.profile.authorised_listings_booked:
                        #             user.profile.authorised_listings_leads.append(listing.id)
                    user.save()

        return Response(status=status.HTTP_200_OK)


def load_and_store_new_listings(city, today):
    # Load new listings
    try:
        with open('json_data_' + city + '.json') as json_file:
            all_listings = json.load(json_file)
    except:
        print(city, 'failed')
        return

    # If existing listing is expired, delete. 
    # If recently expired, mark it as expired
    # so doesn't just disappear from frontend
    listing_queryset = Listing.objects.filter()
    for listing in listing_queryset:
        # If expired recently
        if listing.expired_date <= today:
            listing.url = 'Listing no longer on the market'
            listing.postcode = 'X'
        # If expired more than 3 days ago
        elif listing.expired_date < today - timedelta(days=3):
            listing.delete() 

    # Delete all past listings (risky, think of a better way)
    # listing_queryset = Listing.objects.filter()
    # Listing.objects.all().delete()
    # for listing in listing_queryset:
    #     listing.delete()

    # Store in DB if new
    for i, listing in enumerate(all_listings):

        # Skip already existing listings in DB
        check_if_already_in_DB = Listing.objects.filter(url=listing['url'])
        if check_if_already_in_DB.exists():
            # If rent is the same, skip
            if check_if_already_in_DB[0].rent == listing['rent']:
                continue
            # Otherwise delete the lisitng, go again
            else:
                check_if_already_in_DB[0].delete()
                # Could have a listing['reduced'] = True here, and do something with that to signal to front end listing is reduced

        city_query = City.objects.filter(name=listing['city'])
        if not city_query.exists():
            city = City(name=listing['city'], country=listing['country'])
            city.save()
        else:
            city = city_query[0]

        bedrooms = listing['bedrooms']
        expenses = listing['rent'] * 1.4
        profit = int(listing['mean_income'] - expenses)
        if profit < 500:
            continue

        breakeven_occupancy = int(expenses / listing['mean_income'] * 100)
        round_profit = np.floor(profit / 1000 )  # profit in 1000's
        
        if round_profit == 0: # If lower than 1000, give profit in 100s
            round_profit = int(np.floor(profit / 100 ))  # profit in 1000's
            labels = [f'{bedrooms} bed', f'{round_profit}00+ profit']
        else:
            labels = [f'{bedrooms} bed', f'{round_profit}k+ profit']

        
        print( f"Postcode: {listing['postcode']} - £{profit}/month")
        
        l = Listing(
                city = city,
                postcode = f"{listing['postcode']}",
                rent = int(listing['rent']),
                breakeven_occupancy = breakeven_occupancy,
                expected_income = int(listing['mean_income']),
                profit = profit,
                description =   f"Expected Occupancy: {int(listing['expected_occupancy'])}%; Agency/Host: {listing['agency_or_host']} - {listing['website']}",
                comments = '',
                bedrooms = bedrooms,
                url = listing['url'],
                labels = labels,
                excel_sheet = int(listing["excel_sheet"].split('Listing_',1)[1]),
            )
        # breakpoint()

        if not Listing.objects.filter(url=listing['url']).exists():
            l.save()
            attachment =    Attachment.objects.create(name = f'due_diligence_{l.id}',
                        src=listing['excel_sheet'],
                        size='1kb',)
            attachment.save()
            l.attachments.add(attachment)
        else:
            print('Listing already exists')