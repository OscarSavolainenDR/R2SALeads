# Takes our Python models and converts them to
# JSON to send to front-end, and vice-versa

from rest_framework import serializers
from ..models import Listing, Notification

# Serializes a response
# class ListingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Listing
#         fields = ('city', 'rent', 'expected_occupancy',
#          'expected_profit', 'break_even_o', 'url', 'website',
#          'agency_or_host', 'address', 'postcode') # The fields we want to return

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ('id', 'city', 'name', 'description', 'rent', 'breakeven_occupancy',
         'attachments', 'comments', 'labels', 'url') # The fields we want to return

