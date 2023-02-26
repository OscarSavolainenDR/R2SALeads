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

from .setup_views import financial_logic

# from celery import shared_task
from backend_v3.celery import app

website_domain = os.getenv('WEBSITE_DOMAIN')


@app.task
def send_email_confirmation_celery(pk):

    print('Getting user')
    user = User.objects.filter(pk=pk)[0]

    print('Running on Celery')
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    # If token has already been used
    email_confirm = ConfirmEmail(token=token, uid=uid, user=user)
    # breakpoint()
    email_confirm.save()

    # SEND EMAIL WITH VERIFICATION CODE
    subject = "Confirm Email - R2SA Leads"
    email_template_name = "email_templates/confirm_email.txt"
    c = {
        "email": user.email,
        'domain': website_domain, 
        'site_name': 'Website',
        "uid": uid,
        "user": user,
        'token': token,
        'protocol': 'http',
    }
    email = render_to_string(email_template_name, c)
    try:   
        send_mail(subject, email, 'contact@r2sa-leads.co.uk' , [user.email], fail_silently=False)
        print(f"Email sent successfully for user {user.email}")
    except Exception as e:
        print(e)
        print('Sending confirmation email failed')
        user.delete()


@app.task
def load_and_store_new_listings_celery(city_name, today):
    # Load new listings
    try:
        print(city_name)
        with open('json_data_' + city_name + '.json') as json_file:
            all_listings = json.load(json_file)
    except:
        print(city_name, 'failed')
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
        print(e)
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
                print('Listing exists already')


@app.task
def update_listings_for_users(today):
    # Add new listings to Users
    print('Adding new listings to users, in celery')
    print('There are more effective ways to do this, e.g. for each user, find cities, then all listings from those cities')
    for listing in Listing.objects.filter():
        # Runs once a day, should catch all new ones.
        # Although more robust to go through all listings
        if listing.created_at <= today:
            # print('Listing:', listing.url, listing.id)
            for user in User.objects.filter(): 
                if user.profile.cities.filter(name=listing.city.name).exists():
                    # print(f'Adding listings to {user.username} leads list')
                    # if listing not in user.profile.user_listings.all():
                        # NOTE: need to set listing status to 0 for that user.
                    user.profile.user_listings.add(listing) # doesn't duplicate
                    # if listing.id not in user.profile.authorised_listings_leads:
                    #     if listing.id not in user.profile.authorised_listings_contacted:
                    #         if listing.id not in user.profile.authorised_listings_booked:
                    #             user.profile.authorised_listings_leads.append(listing.id)
                user.save()
                print(f"Finished {user.username}")


def financial_logic(listing):
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