from django.db import models
from base.models import Customer
from location.models import Location
from subscription.models import Subscription


class Order(models.Model):
    customer = models.ForeignKey(Customer)
    subscription = models.ForeignKey(Subscription)
    fulfilled = models.BooleanField()


class MailOrder(Order):
    tracking_number = models.CharField(max_length=255)


class PickupOrder(Order):
    location = models.ForeignKey(Location)
