
from rest_framework import serializers
from ..models import City

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'country', 'price',
                    'description')

class UnsubscribeSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    id = serializers.IntegerField()
    class Meta:
        model = City
        fields = ('id', 'name')

class AddToBasketSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    id = serializers.IntegerField()

    class Meta:
        model = City
        fields = ('id', 'name')

class GetBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ()

class ReturnBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'price')

class CheckoutBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'price', 'country')