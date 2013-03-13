from django.db import models
from base.models import Customer


class Subscription(models.Model):
    amount = models.FloatField()
    active = models.BooleanField()
    public = models.BooleanField()


class CustomerSubscription(models.Model):
    customer = models.ForeignKey(Customer)
    subscription = models.ForeignKey(Subscription)
