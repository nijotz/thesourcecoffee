from base.models import SiteSetting

SiteSetting.objects.all().delete()
SiteSetting.objects.create(
    key='subscriptions.length',
    description='Number of months a subscription lasts',
    value=3)
