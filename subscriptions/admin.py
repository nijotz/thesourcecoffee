from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from products.models import Product
from subscriptions.models import SubscriptionType, Subscription, CustomerSubscription

admin.site.register(SubscriptionType)
admin.site.register(Subscription)
admin.site.register(CustomerSubscription)
