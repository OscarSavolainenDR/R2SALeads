from __future__ import absolute_import, unicode_literals
from ..models import ConfirmEmail, User, City, Listing
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
import os
import json
import numpy as np


# from celery import shared_task
from backend_v3.celery import app

website_domain = os.getenv('WEBSITE_DOMAIN') 

import logging
logger = logging.getLogger(__name__)


# import logging
# auth_logger = logging.getLogger(__name__)
# auth_logger.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
# file_handler = logging.FileHandler(os.path.join(os.getcwd(),'custom_logs','auth.log'))
# file_handler.setFormatter(formatter)
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)
# auth_logger.addHandler(file_handler)
# auth_logger.addHandler(stream_handler)

# excel_path = os.path.join('excels', f'{city}.xlsx')


# setup_logger = logging.getLogger(__name__)
# setup_logger.setLevel(logging.INFO)
# file_handler = logging.FileHandler(os.path.join(os.getcwd(),'custom_logs','setup.log'))
# file_handler.setFormatter(formatter)
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)
# setup_logger.addHandler(file_handler)
# setup_logger.addHandler(stream_handler)


@app.task
def send_email_confirmation_celery(pk):

    auth_logger.info('Creating confirm email token')
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
        auth_logger.info(f"Sending email for user {user.email}")
        send_mail(subject, email, 'contact@r2sa-leads.co.uk' , [user.email], fail_silently=False)
        auth_logger.info(f"Email sent successfully for user {user.email}")
    except Exception as e:
        auth_logger.error(e)
        auth_logger.error('Sending confirmation email failed')
        email_confirm.delete()


@app.task
def load_and_store_new_listings_celery(city_name, today):
    # Load new listings
    try:
        setup_logger.info(city_name)
        with open(os.path.join('listings_json_data','json_data_' + city_name + '.json')) as json_file:
            all_listings = json.load(json_file)
    except:
        setup_logger.error(city_name, 'failed')
        return

    # Find all DB listings in the given city
    city = City.objects.filter(name=city_name)[0]
    listing_queryset = Listing.objects.filter(city=city)

    # Delete all listings in the desired city, that aren't in the new results (considered to be expired)
    try:
        all_urls_in_json = [listing['url'] for listing in all_listings]
        for db_listing in listing_queryset:
            if db_listing.url not in all_urls_in_json:
                db_listing.delete()
    except Exception as e:
        setup_logger.error('Failed to update listings in {city_name}')
        setup_logger.info(e)
        return

    # Store in DB if new
    for _, listing in enumerate(all_listings):  # iterating through listings in json

        # Skip the listings we already have in the DB (unless rent has changed, in which case we delete it 
        # and treat it as a new listing)
        check_if_already_in_DB = Listing.objects.filter(url=listing['url'])
        if check_if_already_in_DB.exists():
            existing_DB_listing = check_if_already_in_DB[0]

            # The financial data may be updated for this listing, check
            bedrooms, breakeven_occupancy, profit, labels = financial_logic(listing)

            if profit < 500:
                existing_DB_listing.delete()
                continue

            # Update existing DB listing in place
            existing_DB_listing.breakeven_occupancy = breakeven_occupancy
            existing_DB_listing.expected_income = int(listing['mean_income'])
            existing_DB_listing.rent = int(listing['rent'])
            existing_DB_listing.profit = profit
            existing_DB_listing.excel_sheet = int(listing["excel_sheet"].split('Listing_',1)[1])
            existing_DB_listing.labels = labels
            existing_DB_listing.save()

        # New listing
        else:

            bedrooms, breakeven_occupancy, profit, labels = financial_logic(listing)

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

            if not Listing.objects.filter(url=listing['url']).exists():
                l.save()
            else:
                setup_logger.error(f"Listing {listing['url']} exists already")

@app.task
def update_listings_for_users_2():
    """
    Fast version. Add all the new listing we have to their repsective users.
    """
    # Add new listings to Users
    setup_logger.info('Adding new listings to users, in celery')
    for user in User.objects.filter(): 
        listings_user_already_has = user.profile.user_listings.all()
        for city in user.profile.cities.all():
            new_listing_set = Listing.objects.filter(city=city).difference(listings_user_already_has.filter(city=city))
            for listing in new_listing_set:
                user.profile.user_listings.add(listing)
        user.save()

        setup_logger.info(f"Finished {user.username}")


@app.task
def update_listings_for_one_user(user):
    """
    Fast version. Add all the new listing we have to a user.
    """
    # Add new listings to Users
    setup_logger.info(f'Adding new listings to {user.username}, in celery')
    listings_user_already_has = user.profile.user_listings.all()
    for city in user.profile.cities.all():
        setup_logger.info(f'Adding {city.name} to {user.username}')
        new_listing_set = Listing.objects.filter(city=city).difference(listings_user_already_has.filter(city=city))
        for listing in new_listing_set:
            user.profile.user_listings.add(listing)
    user.save()

    setup_logger.info(f"Finished updating listings for {user.username}")


def financial_logic(listing):
    """
    Analyses a listing, and calculates some metrics.
    """
    bedrooms = listing['bedrooms']
    profit = int(0.6 * (listing['mean_income'] - listing['rent']))

    breakeven_occupancy = int((listing['mean_income'] - profit) / listing['mean_income'] * 100)
    round_profit = np.floor(profit / 1000 )  # profit in 1000's
    
    if round_profit == 0: # If lower than 1000, give profit in 100s
        round_profit = int(np.floor(profit / 100 ))  # profit in 1000's
        labels = [f'{bedrooms} bed', f'{round_profit}00+ profit']
    else:
        labels = [f'{bedrooms} bed', f'{round_profit}k+ profit']
    
    # print(f"Rounded income {int(listing['mean_income'])} vs original {(listing['mean_income'])}")
    return bedrooms, breakeven_occupancy, profit, labels