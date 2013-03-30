from subscriptions.models import Plan

Plan.objects.all().delete()
amounts = range(1,11) + [0.5, 0.75]
for lbs in amounts:
    Plan.objects.create(amount=lbs, price=lbs * 150, interval=3)
