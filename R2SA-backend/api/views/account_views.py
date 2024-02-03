from django.shortcuts import render
from rest_framework import generics, status
from ..serializers.account_serializers import GetAccountSettingsSerializer, GetAccountSettingsBillingDataSerializer
from ..models import User, Session
from rest_framework.views import APIView 
from rest_framework.response import Response 
from django.http import JsonResponse
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
import json

class GetAccountSettingsData(APIView):
    serializer_class = GetAccountSettingsSerializer
    # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):

        key = request.headers['Authorization'].split(' ')[1]
        key_query_set = Session.objects.filter(key=key)

        if key_query_set.exists():
            username = key_query_set[0].username
            print(key)

            queryset = User.objects.filter(username=username)
            if queryset.exists():
                user = queryset[0]
                print(f'User {user.username} found!')
            else:
                return Response({'msg': f'User {username} not a valid user'}, status=status.HTTP_401_UNAUTHORIZED) 

            response_data = GetAccountSettingsSerializer(user).data

            return Response(response_data, status=status.HTTP_200_OK)
        return Response({'msg': 'Session data not valid.'}, status=status.HTTP_401_UNAUTHORIZED)
 
 
class UpdatePassword(APIView):
    # serializer_class = UpdatePasswordSerializer
    # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):

        key = request.headers['Authorization'].split(' ')[1]
        key_query_set = Session.objects.filter(key=key)

        if key_query_set.exists():
            username = key_query_set[0].username
            print(key)

            queryset = User.objects.filter(username=username)
            if queryset.exists():
                user = queryset[0]
                print(f'User {user.username} found!')
            else:
                return Response({'msg': f'User {username} not a valid user'}, status=status.HTTP_401_UNAUTHORIZED) 

            # Update password
            if user.password == request.data['password']:
                user.password = request.data['newPassword']
                user.save()
            else:
                return Response({'msg': 'Incorrect password.'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response(status=status.HTTP_200_OK)
        return Response({'msg': 'Session data not valid.'}, status=status.HTTP_401_UNAUTHORIZED)
    