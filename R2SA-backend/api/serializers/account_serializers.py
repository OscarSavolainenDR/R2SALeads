from rest_framework import serializers
from ..models import User

class GetAccountSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class GetAccountSettingsBillingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')