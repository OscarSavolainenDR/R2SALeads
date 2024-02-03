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
from django.contrib.auth import authenticate
# from ...backend_v3.settings import BASE_DIR
from ..tasks import send_email_confirmation_celery, update_listings_for_one_user_celery

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import logging

import os
import stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
website_domain = os.getenv('WEBSITE_DOMAIN')

# import logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
# file_handler = logging.FileHandler(os.path.join('custom_logs','auth.log'))
# file_handler.setFormatter(formatter)
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)
# logger.addHandler(file_handler)
# logger.addHandler(stream_handler)

import logging
logger = logging.getLogger(__name__)


class SignIn(APIView):
    serializer_class = SignInSerializer

    def post(self, request, format=None):

        # Get the request data (login details)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(): # check if data in our post request is valid
            username = serializer.data.get('username')
            given_password = serializer.data.get('password')

            user = authenticate(username=username, password=given_password)
            if not user:
                logger.info('Logging in with username didnt work, trying email')

                # Try and authenticate via email, in case they fed their email in
                user_query = User.objects.filter(email=username)
                if user_query.exists():
                    user_name = user_query[0].username
                    user = authenticate(username=user_name, password=given_password)
                    if not user:
                        return Response({'msg': 'Incorrect login details given.'}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                     return Response({'msg': 'Incorrect login details given.'}, status=status.HTTP_401_UNAUTHORIZED)
            # Successful sign in!

            
            # Create session if it doesn't exist already
            if not self.request.session.exists(self.request.session.session_key):
                self.request.session.create()
                old_sessions = Session.objects.filter(username=username)
                if old_sessions.exists():
                    for session in old_sessions:
                        session.delete()

            # Create new session (awkward way to do it)
            new_session = Session(key=self.request.session.session_key, username=username)
            new_session.save()

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
            logging.error("Sign in didn't pass serializer")
            return Response({'msg': 'Login request not valid.'}, status=status.HTTP_401_UNAUTHORIZED)
         

class SignOut(APIView):
    serializer_class = SignOutSerializer

    def post(self, request, format=None):

        # Get the request data (logout details)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(): # check if data in our post request is valid

            # Successful sign out!
            
            # Delete session if it exists
            if self.request.session.exists(self.request.session.session_key):
                del self.request.session
            key = request.headers['Authorization'].split(' ')[1]
            logger.info(f'Session deleted')
            Session.objects.filter(key=key).delete()

            return Response(status=status.HTTP_200_OK) # Send the logout details to frontend
        else:
            logger.exception('Sign Out didnt pass serializer')
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

            if len(given_password) < 8:
                logger.info('Given password too short')
                return Response({'message': 'Your password must be atleast 8 characters long.'}, status=status.HTTP_400_BAD_REQUEST)

            users_queryset = User.objects.filter(username=username)
            if users_queryset.exists():
                logger.info('User already exists')
                return Response({'message': 'User already exists!'}, status=status.HTTP_400_BAD_REQUEST)
            
            email_queryset = User.objects.filter(email=given_email)
            if email_queryset.exists():
                logger.info('Email already exists')
                return Response({'message': 'Email already in use!'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                validate_email(given_email)
                logger.info('Email successfully validated')
            except ValidationError as e:
                logger.info("bad email, details:", e)
                return Response({'message': 'Email address is not valid.'}, status=status.HTTP_400_BAD_REQUEST)


            # Send stripe a message to create customer.import stripe
            stripe_response = stripe.Customer.create(
                email = given_email,
                name = username
            )

            new_user = User(username=username,
                            email = given_email,
                            )
            new_user.set_password(given_password)
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

            # NOTE: Send email confirmation to them.
            # send_email_confirmation(new_user)
            send_email_confirmation_celery.delay(new_user.pk)

            # Add new listings to User
            update_listings_for_one_user_celery.delay(new_user)

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
            logger.exception('Sign Up didnt pass serializer')
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
                    logger.info(f'Sent reset email for {user.email} successfully')
                    send_mail(subject, email, 'contact@r2sa-leads.co.uk' , [user.email], fail_silently=False)
                    return Response(status=status.HTTP_200_OK)
                except Exception as e:
                    logger.debug(f'Failed to send  email for {user.email}')
                    logger.debug(e)
                    reset_password = ResetPassword.objects.filter(token=token, uid=uid, user=user)
                    reset_password[0].delete()
                    # NOTE: maybe change 400 to 200
                    return Response({'msg':'Sending email failed.'}, status=status.HTTP_400_BAD_REQUEST)

            # All is well, don't let hackers know email isn't vlaid
            logger.error("User doesn't exist: hacker")
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
            logger.info('Rest Password Link: Given:', reset_password.date, '; Expires:', (date.today() + timedelta(days=1)))
            if date.today() > (reset_password.date + timedelta(days=1)):
                logger.info('Reset password link expired')
                return Response({'message': 'Stale forgotten password token, request a new one.'}, status=status.HTTP_401_UNAUTHORIZED)

            user = reset_password.user

            try:
                user.set_password(new_password)
                user.save()
                logger.info(f'Updated password for user {user.username}')
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
                logger.info(f'Email confirmed for user {user.username}')
            except:
                logger.info(f'Email update failed for user {user.username}')
                return Response({'message': 'Email not confirmed'}, status=status.HTTP_400_BAD_REQUEST)

            confirm_email.delete()
            return Response(status=status.HTTP_200_OK)
        logger.info(f'Someone used stale confirm email link')
        return Response({'message': 'Stale forgotten password token, request a new one.'}, status=status.HTTP_401_UNAUTHORIZED)



class GetEmailStatus(APIView):
    def post(self, request, format=None):
        user = authenticate_from_session_key(request)
        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED) 
        
        email_status = user.profile.email_confirmed
        return Response({'email_status': email_status}, status=status.HTTP_200_OK)


class ResendConfirmEmail(APIView):
    def post(self, request, format=None):
        user = authenticate_from_session_key(request)
        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED) 

        # Delete old confirmation email object
        logger.info(f'Deleting old confirmation email object for {user.username}')
        old_confirm = ConfirmEmail.objects.filter(user=user)
        if old_confirm.exists():
            old_confirm[0].delete()

        # Resend new one
        # send_email_confirmation(user)
        logger.info(f'Sending confirmation email for {user.username}')
        send_email_confirmation_celery.delay(user.pk)

        return Response(status=status.HTTP_200_OK)


# def send_email_confirmation(user):
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     token = default_token_generator.make_token(user)

#     # If token has already been used
#     email_confirm = ConfirmEmail(token=token, uid=uid, user=user)
#     # breakpoint()
#     email_confirm.save()

#     # SEND EMAIL WITH VERIFICATION CODE
#     subject = "Confirm Email - R2SA Leads"
#     email_template_name = "email_templates/confirm_email.txt"
#     c = {
#         "email": user.email,
#         'domain': website_domain, 
#         'site_name': 'Website',
#         "uid": uid,
#         "user": user,
#         'token': token,
#         'protocol': 'http',
#     }
#     email = render_to_string(email_template_name, c)
#     try:   
#         send_mail(subject, email, 'contact@r2sa-leads.co.uk' , [user.email], fail_silently=False)
#         logger.info(f"Email sent successfully for user {user.email}")
#     except Exception as e:
#         logger.exception(e)
#         logger.debug('Sending confirmation email ({user.email}) failed')
#         email_confirm.delete()
        


def authenticate_from_session_key(request):
    """
    Takes in request, gets the session key and finds the associated user.
    """

    key = request.headers['Authorization'].split(' ')[1]

    # Have a Serializer HERE!
    key_query_set = Session.objects.filter(key=key)

    if key_query_set.exists():
        username = key_query_set[0].username

        # Load user's details from DB
        queryset = User.objects.filter(username=username) | User.objects.filter(email=username)
        # breakpoint()
        if queryset.exists():
            user = queryset[0]
            logger.info(f'User {user.username} authenticated from session key.')
            return user
        else:
            logger.warn(f'User {user.username} not authenticated from session key.')
            return None
    
    return None


