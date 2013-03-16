from subscriptions.models import Subscription

Subscription.objects.all().delete()
Subscription.objects.create(amount=0.5)
Subscription.objects.create(amount=0.75)
for lbs in range(1,11):
    Subscription.objects.create(amount=lbs)
