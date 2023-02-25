from __future__ import absolute_import, unicode_literals
from ..models import ConfirmEmail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
import os
import json

# from celery import shared_task
from backend_v3.celery import app

website_domain = os.getenv('WEBSITE_DOMAIN')


@app.task
def send_email_confirmation_celery(user):

    print('deserializing')
    user = json.loads(user)

    print('Running on Celery')
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