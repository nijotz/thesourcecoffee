from datetime import datetime, timedelta
from itertools import cycle
from customers.models import Customer
from locations.models import Location
from orders.models import MailOrder, Order, PickupOrder
from subscriptions.models import Subscription

subscriptions = cycle(Subscription.objects.all())
locations = cycle(Location.objects.all())

for customer in Customer.objects.all():

    customer.orders.all().delete()

    subscription = subscriptions.next()
    location = locations.next()

    Order.objects.create(
        customer=customer,
        subscription=subscription,
        fulfilled=None
    )
    MailOrder.objects.create(
        customer=customer,
        subscription=subscription,
        fulfilled=datetime.now() - timedelta(days=7),
        date_sent=datetime.now() - timedelta(days=9),
        tracking_number='124567'
    )
    PickupOrder.objects.create(
        customer=customer,
        subscription=subscription,
        fulfilled=datetime.now() - timedelta(days=14),
        location=location
    )
