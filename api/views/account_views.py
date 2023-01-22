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
    
    # server.get(`${apiPrefix}/account/setting`, schema => {
    #     return schema.db.settingData[0]
    # })
# export const settingData = {
#     profile: {
#         name: 'Ron Vargas',
#         email: 'ronnie_vergas@infotech.io',
#         lang: 'en',
#         syncData: false
#     },
# }



# Ask from Stripe
class GetAccountSettingsBillingData(APIView):
    pass
    # server.get(`${apiPrefix}/account/setting/billing`, schema => {
    #     return schema.db.settingBillingData[0]
    # })
# export const settingBillingData = {
#     paymentMethods: [
#         {
#             cardId: '1',
#             cardHolderName: 'Ron Vargas',
#             cardType: 'VISA',
#             expMonth: '12',
#             expYear: '25',
#             last4Number: '0392',
#             primary: true,
#         },
#         {
#             cardId: '2',
#             cardHolderName: 'Ron Vargas',
#             cardType: 'MASTER',
#             expMonth: '06',
#             expYear: '25',
#             last4Number: '8461',
#             primary: false,
#         }
#     ],
#     otherMethod: [
#         {
#             id: '1',
#             identifier: 'ronnie_vergas@infotech.io',
#             redirect: 'https://www.paypal.com/',
#             type: 'PAYPAL'
#         },
#     ],
#     billingHistory: [
#         {
#             id: '#36223',
#             item: 'Mock premium pack',
#             status: 'pending',
#             amount: 39.9,
#             date: 1639132800
#         },
#         {
#             id: '#34283',
#             item: 'Business board pro subscription',
#             status: 'paid',
#             amount: 59.9,
#             date: 1636790880
#         },
#         {
#             id: '#32234',
#             item: 'Business board pro subscription',
#             status: 'paid',
#             amount: 59.9,
#             date: 1634090880
#         },
#         {
#             id: '#31354',
#             item: 'Business board pro subscription',
#             status: 'paid',
#             amount: 59.9,
#             date: 1631532800
#         },
#     ]
# }

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
    