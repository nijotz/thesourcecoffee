from base.models import SiteSetting

SiteSetting.objects.all().delete()

SiteSetting.objects.create(
    key='subscriptions.length',
    description='Number of months a subscription lasts',
    value=3)

SiteSetting.objects.create(
    key='locations.capacity',
    description='Number of pounds a location can store',
    value=100)

SiteSetting.objects.create(
    key='subscriptions.number_of_orders',
    description='Number of orders received per subscription period',
    value=12)
