from django.shortcuts import render
from rest_framework import generics, status
from ..serializers.notification_serializers import NotificationSerializer
from ..models import Listing, User, Session
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
import os

from .auth_views import authenticate_from_session_key

website_domain = os.getenv('WEBSITE_DOMAIN')

class Feedback(APIView):
    serializer_class = NotificationSerializer

    def post(self, request, format=None): 

        user = authenticate_from_session_key(request)
        
        # SEND EMAIL WITH VERIFICATION CODE
        print('Sending feedback', request.data)
        feedback = request.data

        subject = "Feedback - R2SA Leads"
        email_template_name = "email_templates/feedback_email.txt"
        c = {
            "email": "contact@r2sa-leads.co.uk",
            'domain': website_domain, 
            'site_name': 'Website',
            "user": user.username,
            "user_email": user.email,
            'content': feedback,
            'protocol': 'http',
        }
        email = render_to_string(email_template_name, c)
        try:   
            send_mail(subject, email, 'contact@r2sa-leads.co.uk' , ["contact@r2sa-leads.co.uk"], fail_silently=False)
            print(f"Email sent successfully for user {user.email}")
        except Exception as e:
            print(e)
            print('Sending feedback email failed')
        return Response(status=status.HTTP_200_OK)


