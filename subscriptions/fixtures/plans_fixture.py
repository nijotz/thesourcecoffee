from subscriptions.models import Plan
from subscriptions import forms

Plan.objects.all().delete()
amounts = [num for (num, text) in forms.SUBSCRIPTION_AMOUNT_CHOICES]
intervals = [num for (num, text) in forms.SUBSCRIPTION_INTERVAL_CHOICES]

for lbs in amounts:
    for months in intervals:
        Plan.objects.create(amount=lbs, price=lbs * 150, interval=months)
