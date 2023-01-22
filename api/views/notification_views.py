from django.shortcuts import render
from rest_framework import generics, status
from ..serializers.notification_serializers import NotificationSerializer
from ..models import Listing, User, Notification, Attachment
from rest_framework.views import APIView 
from rest_framework.response import Response 
from django.http import JsonResponse
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
import json

class GetNotificationCount(APIView):
    # serializer_class = NotificationCountSerializer

    # Should we have a session here?
    def get(self, request, format=None):

        # NOTE: should these notifications be per session, not per User?
        # Do so by adding new info for User each time we update DB (with new flag), 
        # and create a Notification for that new info. 
        # Then wipe the notification if it gets selected (need frontend to send some info back)


        username = 'Tim' # request.session['username']
        notification_queryset = Notification.objects.filter(userName=username)
        if notification_queryset.exists():
            packet = {'count': len(notification_queryset)}
            # serialized_q = NotificationCountSerializer(packet).data
            return Response(json.dumps(packet), status=status.HTTP_200_OK) # Send the notification details to frontend
        else:
            return Response({'msg': 'No Notifications'}, status=status.HTTP_404_NOT_FOUND)


class GetNotifications(APIView):
    serializer_class = NotificationSerializer

    def get(self, request, format=None): 

        username = 'Tim' # request.session['username']
        notification_queryset = Notification.objects.filter(userName=username)
        if notification_queryset.exists():
            serialized_q = NotificationSerializer(notification_queryset, many=True).data
            return Response(serialized_q, status=status.HTTP_200_OK) # Send the notification details to frontend
        else:
            return Response({'msg': 'No Notifications'}, status=status.HTTP_404_NOT_FOUND)

