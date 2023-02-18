from django.shortcuts import render
from rest_framework import generics, status
from ..serializers.auth_serializers import SignInSerializer, SignOutSerializer, SignUpSerializer #,ForgotPasswordSerializer
from ..models import Listing, User, City, Subscription, Session, ResetPassword, ConfirmEmail
from rest_framework.views import APIView 
from rest_framework.response import Response 
from django.http import JsonResponse
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
import asyncio
from datetime import date
# from ...backend_v3.settings import BASE_DIR

import os
import stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
# SESSION_KEY = os.getenv('SESSION_KEY')

website_domain = os.getenv('WEBSITE_DOMAIN')

class SignIn(APIView):
    serializer_class = SignInSerializer

    def post(self, request, format=None):

        # Get the request data (login details)
        serializer = self.serializer_class(data=request.data)
        print(serializer)
        if serializer.is_valid(): # check if data in our post request is valid
            username = serializer.data.get('username')
            given_password = serializer.data.get('password')

            users_queryset = User.objects.filter(username=username)
            if users_queryset.exists():
                user = users_queryset[0]
                if user.password != given_password:
                    print('first')
                    return Response({'msg': 'Incorrect login details given.'}, status=status.HTTP_401_UNAUTHORIZED)
                
                # Successful sign in!

                # print('Token:', SESSION_KEY)
                
                # Create session if it doesn't exist already
                if not self.request.session.exists(self.request.session.session_key):
                    self.request.session.create()
                    old_sessions = Session.objects.filter(username=username)
                    if old_sessions.exists():
                        for session in old_sessions:
                            session.delete()

                # Create new session (awkward way to do it)
                # print(self.request.session.session_key)
                # print(len(self.request.session.session_key))
                new_session = Session(key=self.request.session.session_key, username=username)
                new_session.save()

                # request.session['username'] = username

                return Response({
                                'user': {
                                    'avatar': '',
                                    'username': username,
                                    'email': user.email,
                                    'authority': user.profile.authorisations,
                                },
                                'token': self.request.session.session_key, # SESSION_KEY
                                }, status=status.HTTP_200_OK) # Send the notification details to frontend
            else:
                print('second', username)
                return Response({'msg': 'User name not found in database.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            print('didnt pass serializer')
            return Response({'msg': 'Login request not valid.'}, status=status.HTTP_401_UNAUTHORIZED)
         

class SignOut(APIView):
    serializer_class = SignOutSerializer

    def post(self, request, format=None):

        # Get the request data (logout details)
        serializer = self.serializer_class(data=request.data)
        print(serializer, request.data)
        if serializer.is_valid(): # check if data in our post request is valid

            # Successful sign out!
            
            # Delete session if it exists
            if self.request.session.exists(self.request.session.session_key):
                del self.request.session

            print('Session deleted')
            key = request.headers['Authorization'].split(' ')[1]
            Session.objects.filter(key=key).delete()

            return Response(status=status.HTTP_200_OK) # Send the logout details to frontend
        else:
            print('Sign Out didnt pass serializer')
            return Response({'Bad Request': 'Logout request not valid.'}, status=status.HTTP_400_BAD_REQUEST)
         

class SignUp(APIView):
    serializer_class = SignUpSerializer

    def post(self, request, format=None):

        # Get the request data (logout details)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(): # check if data in our post request is valid

            username = serializer.data.get('username')
            given_password = serializer.data.get('password')
            given_email = serializer.data.get('email')

            users_queryset = User.objects.filter(username=username)
            if users_queryset.exists():
                errors = [{'message': '', 'domain': "global", 'reason': "invalid"}]
                packet = errors, {'message': 'User already exists!'}
                print('User already exists')
                return Response(json.dumps(packet), status=status.HTTP_400_BAD_REQUEST)
            
            email_queryset = User.objects.filter(email=given_email)
            if email_queryset.exists():
                # errors = [{'message': '', 'domain': "global", 'reason': "invalid"}]
                # packet = errors, {'message': 'Email already in use!'}
                print('Email already exists')
                # print(json.dumps(packet))
                return Response({'message': 'Email already in use!'}, status=status.HTTP_400_BAD_REQUEST)

            # Send stripe a message to create customer.import stripe
            stripe_response = stripe.Customer.create(
                email = given_email,
                name = username
            )

            new_user = User(username=username,
                            password=given_password,
                            email = given_email,
                            )
            new_user.save()
            # new_user.profile.authorisations = ['user'],
            new_user.profile.stripe_customer_id = stripe_response.id
            new_user.save()
            # new_user.profile.authorised_listings_leads = [],
            # new_user.profile.authorised_listings_contacted = [],
            # new_user.profile.authorised_listings_booked = [],
            # new_user.set_cities()

            # Create subscription to Oxford (default)
            city = City.objects.filter(name='Oxford')[0]
            Subscription.objects.create(user=new_user.profile, city=city)

            # Add new listings to User
            for listing in Listing.objects.filter(city=city):
                if listing.created_at <= date.today():
                    if listing not in new_user.profile.user_listings.all():
                        # NOTE: need to set listing status to 0 for that user.
                        new_user.profile.user_listings.add(listing)
            new_user.save()

            # NOTE: Send email confirmation to them.
            send_email_confirmation(new_user)

            packet = {
                'username': username,
                'avatar': 'null',
                'authority': new_user.profile.authorisations,
                'email': given_email,
            }

            packet = {
                'user': packet,
                'token': self.request.session.session_key,
            }
            packet = json.dumps(packet)

            return Response(packet, status=status.HTTP_200_OK) # Send the logout details to frontend
        else:
            print('Sign Up didnt pass serializer')
            return Response({'message': 'Email or username already in use.'}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPassword(APIView):
    # serializer_class = ForgotPasswordSerializer
    # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):

        # NOTE: no auth
        # print(request.data)
        # serializer = self.serializer_class(data=request.data)
        # print(serializer)
        # if serializer.is_valid(): # check if data in our post request is valid (should just be email)

            # email = serializer.data.get('email')
            email = request.data['email']
            user_set = User.objects.filter(email=email)

            if user_set.exists():
                user = user_set[0]

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)

                # # If token has already been used
                # if ResetPassword.objects.filter(token=token, uid=uid).exists():
                #     # return Response({'msg': 'Error: stale request.'}, status=status.HTTP_400_BAD_REQUEST)
                # # ResetPassword.objects.create(token=token, uid=uid)
                #     pass
                ResetPassword.objects.create(token=token, uid=uid, user=user)
                # r.save()
 
                # SEND EMAIL WITH VERIFICATION CODE
                # r = ResetPassword(user=user, email=email)

                subject = "Password Reset Requested"
                email_template_name = "email_templates/password_reset_email.txt"
                c = {
                    "email":user.email,
                    'domain':website_domain,
                    'site_name': 'Website',
                    "uid": uid,
                    "user": user,
                    'token': token,
                    'protocol': 'http',
                }
                email = render_to_string(email_template_name, c)
                try:  
                    print('Sent reset email successfully')
                    send_mail(subject, email, 'contact@r2sa-leads.co.uk' , [user.email], fail_silently=False)
                    return Response(status=status.HTTP_200_OK)
                except Exception as e:
                    print(e)
                    reset_password = ResetPassword.objects.filter(token=token, uid=uid, user=user)
                    reset_password[0].delete()
                    # NOTE: maybe change 400 to 200
                    return Response({'msg':'Sending email failed.'}, status=status.HTTP_400_BAD_REQUEST)

            # All is well, don't let hackers know email isn't vlaid
            print("user doesn't exist")
            return Response(status=status.HTTP_200_OK)
        # return Response({'msg': 'Session data not valid.'}, status=status.HTTP_401_UNAUTHORIZED)

class ResetPasswordView(APIView):
    # serializer_class = PasswordSerializer
    # lookup_url_kwarg = 'code' # when we call this instance, we need to give a keyword arguement

    # Define a get request: frontend asks for stuff
    def post(self, request, format=None):

        # print(request.data)
        uid = request.data['uid']
        token = request.data['token']
        new_password = request.data['password'] 

        # NOTE: need to check it's valid password, although I guess done in model field.

        query_set = ResetPassword.objects.filter(uid=uid, token=token)
        if query_set.exists():
            reset_password = query_set[0] 

            from datetime import date, timedelta
            print('Given:', reset_password.date, '; Expires:', (date.today() + timedelta(days=1)))
            if date.today() > (reset_password.date + timedelta(days=1)):
                print('Old')
                return Response({'message': 'Stale forgotten password token, request a new one.'}, status=status.HTTP_401_UNAUTHORIZED)

            user = reset_password.user

            try:
                user.password = new_password
                user.save()
                print('Updated password')
            except:
                return Response({'message': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

            reset_password.delete()
            return Response(status=status.HTTP_200_OK)
        return Response({'message': 'Stale forgotten password token, request a new one.'}, status=status.HTTP_401_UNAUTHORIZED)


class ConfirmEmail_api(APIView):
    def post(self, request, format=None):
        # print(request.data)
        uid = request.data['uid']
        token = request.data['token']

        query_set = ConfirmEmail.objects.filter(uid=uid, token=token)
        if query_set.exists():
            confirm_email = query_set[0] 

            # from datetime import date, timedelta
            # print('Given:', confirm_email.date, '; Expires:', (date.today() + timedelta(days=1)))
            # if date.today() > (reset_password.date + timedelta(days=1)):
            #     print('Old')
            #     return Response({'message': 'Stale forgotten password token, request a new one.'}, status=status.HTTP_401_UNAUTHORIZED)

            user = confirm_email.user

            try:
                user.profile.email_confirmed = True
                user.save()
                print('Email confirmed')
            except:
                print('Email update failed')
                return Response({'message': 'Email not confirmed'}, status=status.HTTP_400_BAD_REQUEST)

            confirm_email.delete()
            return Response(status=status.HTTP_200_OK)
        print('queryset does not exist')
        return Response({'message': 'Stale forgotten password token, request a new one.'}, status=status.HTTP_401_UNAUTHORIZED)

class GetEmailStatus(APIView):
    def post(self, request, format=None):
        key = request.headers['Authorization'].split(' ')[1]
        # Have a Serializer HERE!
        key_query_set = Session.objects.filter(key=key)

        if key_query_set.exists():
            username = key_query_set[0].username

            # Load user's details from DB
            queryset = User.objects.filter(username=username)
            if queryset.exists():
                user = queryset[0]
                print(f'User {user.username} found!')
            else:
                return Response({'msg': f'User {username} not a valid user'}, status=status.HTTP_401_UNAUTHORIZED) 

            email_status = user.profile.email_confirmed
            return Response({'email_status': email_status}, status=status.HTTP_200_OK)


def send_email_confirmation(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    # If token has already been used
    email_confirm = ConfirmEmail(token=token, uid=uid, user=user)
    # breakpoint()
    email_confirm.save()

    # SEND EMAIL WITH VERIFICATION CODE
    subject = "Confirm Email - R2SA Leads"
    email_template_name = "email_templates/confirm_email.txt"
    c = {
        "email": user.email,
        'domain': website_domain, 
        'site_name': 'Website',
        "uid": uid,
        "user": user,
        'token': token,
        'protocol': 'http',
    }
    email = render_to_string(email_template_name, c)
    try:   
        send_mail(subject, email, 'contact@r2sa-leads.co.uk' , [user.email], fail_silently=False)
        print(f"Email sent successfully for user {user.email}")
    except Exception as e:
        print(e)
        print('Sending confirmation email failed')
        user.delete()
        


