from products.models import Product
from subscriptions.models import Subscription, SubscriptionType

for amount in (4, 8, 12, 20, 50):
    try:
        SubscriptionType.objects.filter(amount=amount, period=14).delete()
    except SubscriptionType.DoesNotExist:
        pass

    SubscriptionType.objects.create(amount=amount, period=14)

for product in Product.objects.all():
    for sub_type in SubscriptionType.objects.all():
        try:
            Subscription.objects.filter(
                subscription_type=sub_type,
                product=product
            ).delete()
        except Subscription.DoesNotExist:
            pass

        Subscription.objects.create(
            subscription_type=sub_type,
            product=product,
            price=50.00)
