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
class Test(APIView):
    today = date.today()
    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):
        customer_id = 'cus_NMxxbwMleAlWt5'
        # queryset = User.objects.filter()
        queryset = User.objects.get(profile__stripe_customer_id=customer_id)

        print(queryset) 
        print(queryset[0].profile.stripe_customer_id)

        return Response(status=status.HTTP_200_OK) 