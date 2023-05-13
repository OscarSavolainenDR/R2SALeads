from __future__ import absolute_import, unicode_literals
from .models import ConfirmEmail, User, City, Listing
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
import os
import json
import numpy as np
import gzip


# from celery import shared_task
# from backend_v3.celery import app
from celery import shared_task

from .views.cities import cities as cities

website_domain = os.getenv('WEBSITE_DOMAIN') 

import logging
logger = logging.getLogger(__name__)


# import logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
# file_handler = logging.FileHandler(os.path.join(os.getcwd(),'custom_logs','auth.log'))
# file_handler.setFormatter(formatter)
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)
# logger.addHandler(file_handler)
# logger.addHandler(stream_handler)

# excel_path = os.path.join('excels', f'{city}.xlsx')


# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# file_handler = logging.FileHandler(os.path.join(os.getcwd(),'custom_logs','setup.log'))
# file_handler.setFormatter(formatter)
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)
# logger.addHandler(file_handler)
# logger.addHandler(stream_handler)

# # NOTE: For celery, we use app directly, since we're on Heroku and
# # I'm not sure shared_app will work.

@shared_task()
def send_email_confirmation_celery(pk):

    logger.info('Creating confirm email token')
    user = User.objects.filter(pk=pk)[0]

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    email_confirm = ConfirmEmail(token=token, uid=uid, user=user)
    email_confirm.save()

    # SEND EMAIL WITH VERIFICATION CODE
    subject = "Confirm Email - R2SA Leads"
    email_template_name = "email_templates/confirm_email.txt"
    c = {
        "email": user.email,
        'domain': website_domain, 
        "uid": uid,
        "user": user,
        'token': token,
        'protocol': 'https',
    }
    email = render_to_string(email_template_name, c)
    try:   
        logger.info(f"Sending email for user {user.email}")
        send_mail(subject, email, 'contact@r2sa-leads.co.uk' , [user.email], fail_silently=False)
        logger.info(f"Email sent successfully for user {user.email}")
    except Exception as e:
        logger.error(e)
        logger.error('Sending confirmation email failed')
        email_confirm.delete()


@shared_task()
def load_and_store_new_listings_celery(city_name):
    # Load new listings
    try:
        logger.info(city_name)
        # with open(os.path.join('listings_json_data','json_data_' + city_name + '_debug.json')) as json_file:
        #     all_listings = json.load(json_file)
        with gzip.open(os.path.join('listings_json_data','json_data_' + city_name + '.json'), 'r') as fin:
            all_listings = json.loads(fin.read().decode('utf-8'))
    except:
        logger.error(city_name, 'failed')
        return

    # Find all DB listings in the given city
    city = City.objects.filter(name=city_name)[0]
    listing_queryset = Listing.objects.filter(city=city)

    # Delete all listings in the desired city, that aren't in the new results (considered to be expired)
    try:
        all_urls_in_json = [listing[0]['Listing URL'] for listing in all_listings]
        for db_listing in listing_queryset:
            if db_listing.url not in all_urls_in_json:
                db_listing.delete()
    except Exception as e:
        logger.error('Failed to delete listings-absent-from-update in {city_name}')
        logger.info(e)
        return

    # Store in DB if new
    for listing_index, listing in enumerate(all_listings):  # iterating through listings in json

        # Convert JSON to pandas
        import pandas as pd
        listing = pd.read_json(json.dumps(listing))

        # Skip the listings we already have in the DB (unless rent has changed, in which case we delete it 
        # and treat it as a new listing)
        check_if_already_in_DB = Listing.objects.filter(url=listing['Listing URL'].iloc[0])
        if check_if_already_in_DB.exists():
            existing_DB_listing = check_if_already_in_DB[0]

            # The financial data may be updated for this listing, check
            bedrooms, breakeven_occupancy, profit, labels = financial_logic(listing)

            if profit < 500:
                existing_DB_listing.delete()
                continue

            # Update existing DB listing in place
            existing_DB_listing.breakeven_occupancy = breakeven_occupancy
            existing_DB_listing.expected_income = int(listing['Mean Monthly Income'].iloc[0])
            existing_DB_listing.rent = int(30*listing['Listing Daily Rent'].iloc[0])
            existing_DB_listing.profit = profit
            existing_DB_listing.labels = labels
            existing_DB_listing.excel_sheet = listing_index # important that this index is correct
            existing_DB_listing.save()

        # New listing
        else:

            bedrooms, breakeven_occupancy, profit, labels = financial_logic(listing)

            l = Listing(
                city = city,
                # postcode = f"{listing['postcode']}",
                rent = int(30*listing['Listing Daily Rent'].iloc[0]),
                breakeven_occupancy = breakeven_occupancy,
                expected_occupancy = int(listing['Occupancy (%)'].iloc[0]),
                expected_income = int(listing['Mean Monthly Income'].iloc[0]),
                profit = profit,
                description =   f"Expected Occupancy: {int(listing['Occupancy (%)'].iloc[0])}%; Agency/Host: Temp",
                comments = '',
                bedrooms = bedrooms,
                url = listing['Listing URL'].iloc[0],
                labels = labels,
                excel_sheet = listing_index, # don't use this, can be unreliable. Use URL as index, it's cleaner.
            )

            if not Listing.objects.filter(url=listing['Listing URL'].iloc[0]).exists():
                l.save()
            else:
                logger.error(f"Listing {listing['Listing URL'].iloc[0]} exists already")

@shared_task()
def update_listings_for_users_2_celery():
    """
    Fast version. Add all the new listings we have to their repsective users.
    """
    # Add new listings to Users
    logger.info('Adding new listings to users, in celery')
    for user in User.objects.filter(): 
        listings_user_already_has = user.profile.user_listings.all()
        for city in user.profile.cities.all():
            new_listing_set = Listing.objects.filter(city=city).difference(listings_user_already_has.filter(city=city))
            for listing in new_listing_set:
                user.profile.user_listings.add(listing)
        user.save()

        logger.info(f"Finished {user.username}")


@shared_task()
def update_listings_for_one_user_celery(user):
    """
    Fast version. Add all the new listing we have to a user.
    """
    # Add new listings to Users
    logger.info(f'Adding new listings to {user.username}, in celery')
    listings_user_already_has = user.profile.user_listings.all()
    for city in user.profile.cities.all():
        logger.info(f'Adding {city.name} to {user.username}')
        new_listing_set = Listing.objects.filter(city=city).difference(listings_user_already_has.filter(city=city))
        for listing in new_listing_set:
            user.profile.user_listings.add(listing)
    user.save()

    logger.info(f"Finished updating listings for {user.username}")

@shared_task()
def update_listings_master_celery():
    for city in cities:
        if type(city) is tuple:
            city = city[0]
        load_and_store_new_listings_celery.delay(city['name'])

    update_listings_for_users_2_celery()


def financial_logic(listing):
    """
    Analyses a listing, and calculates some metrics.
    """
    bedrooms = int(listing['Listing Bedrooms'].iloc[0])
    mean_income = int(listing['Mean Monthly Income'].iloc[0])
    profit = int(0.6 * (mean_income - listing['Listing Daily Rent'].iloc[0]))

    breakeven_occupancy = int((mean_income - profit) / mean_income * 100)
    round_profit = np.floor(profit / 1000 )  # profit in 1000's
    
    if round_profit == 0: # If lower than 1000, give profit in 100s
        round_profit = int(np.floor(profit / 100 ))  # profit in 1000's
        labels = [f'{bedrooms} bed', f'{round_profit}00+ profit']
    else:
        labels = [f'{bedrooms} bed', f'{round_profit}k+ profit']
    
    # print(f"Rounded income {int(listing['mean_income'])} vs original {(listing['mean_income'])}")
    return bedrooms, breakeven_occupancy, profit, labels