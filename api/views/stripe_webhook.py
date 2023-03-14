import json
from django.http import HttpResponse
import stripe
from django.views.decorators.csrf import csrf_exempt
import os
from datetime import date
from .celery_tasks import update_listings_for_one_user

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')

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
        print(e)
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
        print('Customer created, yay')
        # customer_email = event.data.object.email
        # cusotmer_id = event.data.object.id

    elif event.type == 'customer.subscription.deleted':
        print('Subscription deleted')
        # print(event)
    elif event.type == 'customer.subscription.created':
        print('Subscription created')
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
        print('Subscription updated')
        # breakpoint()
    elif event.type == 'invoice.payment_failed':
        print('Payment failed')
    elif event.type == 'invoice.payment_succeeded':
        print('Payment succeeded')

        print('We confirm their subscription')
        # print(event)
        customer_id = event.data.object.customer
        customer_email = event.data.object.customer_email
        from ..models import Profile, City, Subscription, User, Listing

        # We find user form customer id
        print('Customer ID:', customer_id, '; Email:', customer_email)
        # queryset = User.objects.filter(profile__stripe_customer_id=customer_id)
        queryset = User.objects.filter(email=customer_email)
        if queryset.exists():
            user = queryset[0]
            print('User:', user.email)
        else:
            print('User not found')

        # We iterate through subscriptions, add them to user
        # print('Lines:', event.data.object.lines.data)
        for elem in event.data.object.lines.data:
            # Price code
            print('price code', elem.price.id)
            subscription_id = elem.subscription_item
            city_queryset = City.objects.filter(stripe_subscription_code=elem.price.id)
            if city_queryset.exists():
                city = city_queryset[0]
                print(f'City {city.name} identified')
                print('subscription id', subscription_id)

                # Create subscription
                if not Subscription.objects.filter(user=user.profile, city=city).exists():
                    Subscription.objects.create(user=user.profile, city=city, stripe_subscription_id=subscription_id)
                print('We got here')

                # Delete from basket
                user.profile.cities_basket.remove(city)

                print('User basket', user.profile.cities_basket)
                print('User cities', user.profile.cities)

                print('Adding listings to user')
                update_listings_for_one_user(user)
                #  # Add new listings to User
                # for listing in Listing.objects.filter(city=city):
                #     if listing.created_at <= date.today():
                #         if listing not in user.profile.user_listings.all():
                #             # NOTE: need to set listing status to 0 for that user.
                #             user.profile.user_listings.add(listing)
                user.save()
        
        print('all user cities', user.profile.cities.all())

    else:
        print('Unhandled event type {}'.format(event.type))


    # breakpoint()
    # print(event)

    return HttpResponse(status=200)