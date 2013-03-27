from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from subscriptions.models import Plan, Subscription

admin.site.register(Plan)
admin.site.register(Subscription)
