from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from subscriptions.models import Subscription, CustomerSubscription

admin.site.register(Subscription)
admin.site.register(CustomerSubscription)
