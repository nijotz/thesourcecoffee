from mezzanine.pages.models import Page
from products.models import Product
from subscriptions.models import Subscription, SubscriptionType

SubscriptionType.objects.create(amount=4, period=14)
SubscriptionType.objects.create(amount=8, period=14)
SubscriptionType.objects.create(amount=12, period=14)
SubscriptionType.objects.create(amount=20, period=14)
SubscriptionType.objects.create(amount=50, period=14)

for product in Product.objects.all():
    for sub_type in SubscriptionType.objects.all():
        Subscription.objects.create(
            subscription_type=sub_type,
            product=product,
            price=50.00)
