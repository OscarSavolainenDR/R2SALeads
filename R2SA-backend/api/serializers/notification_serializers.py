from rest_framework import serializers
from ..models import Notification
 
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'target', 'description', 'date', 'image', 'type', 'location',
                'locationLabel', 'status', 'readed')