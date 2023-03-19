from django.db import models
# from django_random_id_model import RandomIDModel
from django.contrib.postgres.fields import ArrayField
import random, string
from datetime import date, timedelta, datetime
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

def generate_unique_code():
    length = 16
    while True:
        id = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Listing.objects.filter(id=id).count() == 0:
            break
    return id
    
def generate_unique_code_notification():
    length = 16
    while True:
        id = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Notification.objects.filter(id=id).count() == 0:
            break
    return id

def get_list_default():
    return []

class City(models.Model):
    name = models.CharField(max_length=30, unique=True)
    country = models.CharField(max_length=30)
    price = models.IntegerField(null=False, default=50)
    # status = models.IntegerField(null=False, default=2)
    # tags = ArrayField(models.CharField(max_length=20)) # e.g beds
    # portal = models.CharField(max_length=30) # e.g zoopla
    description = models.CharField(max_length=200) # quant description of city
    stripe_subscription_code = models.CharField(max_length=40, unique=True)


class Listing(models.Model): #RandomIDModel
    # today = date.today()

    def future_date():
        return date.today() + timedelta(days=60)
    id = models.CharField(primary_key=True, max_length=18, default=generate_unique_code, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    postcode = models.CharField(max_length=10)
    description = models.CharField(max_length=1000)
    expected_income = models.IntegerField(default=50)
    profit = models.IntegerField(default=50)
    rent = models.IntegerField(default=50)
    expected_occupancy = models.IntegerField(default=50)
    breakeven_occupancy = models.IntegerField(default=110)
    comments = models.CharField(max_length=250)
    bedrooms = models.IntegerField(default=50)
    labels = ArrayField(models.CharField(max_length=15, unique=False))
    expired_date = models.DateField(default=future_date)
    url = models.CharField(max_length=250, unique=True, null=True)
    created_at = models.DateField(default=now)
    excel_sheet = models.IntegerField(default=0)

    attachments = models.ManyToManyField('Attachment',
                                     related_name='attachments_to_listing')

class Profile(models.Model):

    # Details on listings
    cities = models.ManyToManyField('City',
                                     through='Subscription')

    cities_basket = models.ManyToManyField('City',
                                     through='Basket', related_name='cities_in_basket')

    # cities = ArrayField(models.CharField(max_length=30, blank=True))
    user_listings = models.ManyToManyField('Listing',
                                     through='Authorised_Listings')

    stripe_customer_id = models.CharField(max_length=30)
    # authorised_listings_leads = ArrayField( models.CharField(max_length=18, unique=True), default=get_list_default)
    # authorised_listings_contacted = ArrayField( models.CharField(max_length=18, unique=True), default=get_list_default)
    # authorised_listings_booked = ArrayField( models.CharField(max_length=18, unique=True), default=get_list_default) # Viewing booked
    sign_up_date = models.DateField(auto_now_add=True)

    # Sign in authorisations
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # user_name = models.CharField(max_length=30, unique=True)
    # email = models.EmailField(max_length=30, unique=True, blank=False)
    authorisations = ArrayField(models.CharField(max_length=20), default=get_list_default)
    # password = models.CharField(max_length=20, blank=False)

    email_confirmed = models.BooleanField(default=False)

    # trial_week_start = models.DateField()
    # trial_city = models.ForeignKey(City, on_delete=models.CASCADE,
    #                         related_name='trial_city')

    # Should have some function that makes sure there's no overlap between leads and contacted
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Subscription(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    status = models.IntegerField(null=False, default=2)  # unused
    subscription_date = models.DateField(auto_now_add=True)
    stripe_subscription_id = models.CharField(max_length=40)

# Subscription checkout basket
class Basket(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE) # may need to be User instance
    city = models.ForeignKey(City, on_delete=models.CASCADE)

class Attachment(models.Model):
    id = models.CharField(primary_key=True, max_length=18, default=generate_unique_code, unique=True) # same codeword base as Listings, since both may be draggable objects, buit could be its own base
    name = models.CharField(max_length=30)
    src = models.CharField(max_length=30) #FileField(upload_to='due_diligence') # path to excel, but really should be whole file.
    size = models.CharField(max_length=8)
    # key = models.CharField(max_length=18, default=generate_unique_code, unique=True)


class Notification(models.Model):
    id = models.CharField(max_length=18, default=generate_unique_code_notification, unique=True, primary_key=True)
    userName = models.CharField(max_length=10)
    target = models.CharField(max_length=10)
    description = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    image = models.ImageField()
    type = models.IntegerField(null=False, default=0)
    location = models.CharField(max_length=10)
    locationLabel = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    readed = models.BooleanField(null=False, default=False)

class Session(models.Model):
    key = models.CharField(max_length=32, unique=True, primary_key=True)
    username = models.CharField(max_length=30, unique=True)

class ResetPassword(models.Model):
    token = models.CharField(max_length=50, unique=True)
    uid = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

class ConfirmEmail(models.Model):
    token = models.CharField(max_length=50, unique=True)
    uid = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

class Authorised_Listings(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    status = models.IntegerField(null=False, default=0)  # lead, contacted or viewing booked