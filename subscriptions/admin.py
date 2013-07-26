from django.contrib import admin
from subscriptions.models import Plan, Subscription
from base.models import SiteSetting

admin.site.register(Plan)
admin.site.register(Subscription)

# TODO: This doesn't belong here, but it doesn't work in base/admin.py
admin.site.register(SiteSetting)
