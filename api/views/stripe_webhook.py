import json
from django.http import HttpResponse
import stripe
from django.views.decorators.csrf import csrf_exempt
import os
from datetime import date
from .celery_tasks import update_listings_for_one_user

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')

# import logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
# file_handler = logging.FileHandler(os.path.join(os.getcwd(),'custom_logs','stripe_webhook.log'))
# file_handler.setFormatter(formatter)
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)
# logger.addHandler(file_handler)
# logger.addHandler(stream_handler)

import logging
logger = logging.getLogger(__name__)


# Using Django
@csrf_exempt
def stripe_webhook(request):

    payload = request.body.decode('utf-8')
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        # event = stripe.Event.construct_from(
        #   json.loads(payload), stripe.api_key
        # )
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except Exception as e:
        logger.error('Failed to construct webhook event')
        logger.debug(e)
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object # contains a stripe.PaymentIntent
        # Then define and call a method to handle the successful payment intent.
        # handle_payment_intent_succeeded(payment_intent)
    elif event.type == 'payment_method.attached':
        payment_method = event.data.object # contains a stripe.PaymentMethod
        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)
        # ... handle other event types

    elif event.type == 'customer.created':
        logger.info('Customer created, yay')
        logger.info(event)
        # customer_email = event.data.object.email
        # cusotmer_id = event.data.object.id

    elif event.type == 'customer.subscription.deleted':
        logger.info('Subscription deleted')
        logger.info(event)
        # print(event)
    elif event.type == 'customer.subscription.created':
        logger.info('Subscription created')
        logger.info(event)
        # customer_id = event.data.object.customer
        # subscription_id = event.data.object.id
        # from ..models import Profile, City, Subscription
        # queryset = Profile.objects.filter(stripe_customer_id=cusotmer_id)
        # if queryset.exists():
        #     user = queryset[0].user

        # # city_queryset = City.objects.filter(stripe_subscription_code=)
        # if city_queryset.exists():
        #     city = city_queryset[0]
        #     user.profile.cities.add(city)

        #     Subscription.objects.create(user=user.profile, city=city, stripe_subscription_id=subscription_id)
        
        
        # print(f'Customer {customer_id} has subscription {subscription_id}')
        # breakpoint()
        # print(event)
    elif event.type == 'customer.subscription.updated':
        logger.info('Subscription updated')
        logger.info(event)
        # breakpoint()
    elif event.type == 'invoice.payment_failed':
        logger.info('Payment failed')
        logger.info(event)
    elif event.type == 'invoice.payment_succeeded':
        logger.info('Payment succeeded')
        logger.info(event)

        logger.info('We confirm their subscription')
        # print(event)
        customer_id = event.data.object.customer
        customer_email = event.data.object.customer_email
        from ..models import Profile, City, Subscription, User, Listing

        # We find user form customer id
        logger.info('Customer ID:', customer_id, '; Email:', customer_email)
        # queryset = User.objects.filter(profile__stripe_customer_id=customer_id)
        queryset = User.objects.filter(email=customer_email)
        if queryset.exists():
            user = queryset[0]
            logger.info('Found corresponding user:', user.email)
        else:
            logger.error('User not found')

        # We iterate through subscriptions, add them to user
        # print('Lines:', event.data.object.lines.data)
        for elem in event.data.object.lines.data:
            # Price code
            # print('price code', elem.price.id)
            subscription_id = elem.subscription_item
            city_queryset = City.objects.filter(stripe_subscription_code=elem.price.id)
            if city_queryset.exists():
                city = city_queryset[0]
                # print(f'City {city.name} identified')
                # print('subscription id', subscription_id)

                logger.info(f"Creating subscription for {user.username} for {city.name}")

                # Create subscription
                if not Subscription.objects.filter(user=user.profile, city=city).exists():
                    Subscription.objects.create(user=user.profile, city=city, stripe_subscription_id=subscription_id)
                logger.info(f"Subscription option created for {user.username} for {city.name}")

                # Delete from basket
                user.profile.cities_basket.remove(city)
                logger.info(f"Deleted {city.name} from basket for {user.username}")

                logger.info('{user.username} basket', user.profile.cities_basket)
                logger.info('{user.username} cities', user.profile.cities)

        update_listings_for_one_user(user)
        user.save()
        
        logger.info('All {user.username} cities:', user.profile.cities.all())

    else:
        logger.debug('Unhandled event type {}'.format(event.type))
    return HttpResponse(status=200)