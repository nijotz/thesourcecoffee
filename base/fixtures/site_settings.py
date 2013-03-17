from base.models import SiteSetting

SiteSetting.objects.create(
    key='subscription.length',
    description='Number of days a subscription lasts',
    value=7)
