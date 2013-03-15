from django.db import models
from model_utils.managers import InheritanceManager
from customers.models import Customer
from locations.models import Location
from subscriptions.models import Subscription


class Order(models.Model):
    customer = models.ForeignKey(Customer, related_name='orders')
    subscription = models.ForeignKey(Subscription)
    fulfilled = models.DateTimeField(null=True)

    objects = InheritanceManager()


class MailOrder(Order):
    tracking_number = models.CharField(max_length=255)
    date_sent = models.DateTimeField()


class PickupOrder(Order):
    location = models.ForeignKey(Location)
