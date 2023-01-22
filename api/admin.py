from django.contrib import admin

# Register your models here.
from .models import City, Listing, Profile, Basket, Subscription, Session, ResetPassword, Attachment

admin.site.register(City)
admin.site.register(Listing)
admin.site.register(Profile)
admin.site.register(Basket)
admin.site.register(Subscription)
admin.site.register(Session)
admin.site.register(ResetPassword)
admin.site.register(Attachment)
