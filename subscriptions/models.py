from django.db import models
from django.contrib.auth.models import User


class Subscription(models.Model):
    amount = models.FloatField()


class CustomerSubscription(models.Model):
    customer = models.ForeignKey(User)
    subscription = models.ForeignKey(Subscription)
    custom_amount = models.IntegerField()
