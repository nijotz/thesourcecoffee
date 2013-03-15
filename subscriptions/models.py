from django.db import models
from customers.models import Customer


class Subscription(models.Model):
    amount = models.FloatField()
    active = models.BooleanField()
    public = models.BooleanField()

    def __unicode__(self):
        return '%d ozs' % (self.amount)


class CustomerSubscription(models.Model):
    customer = models.ForeignKey(Customer)
    subscription = models.ForeignKey(Subscription)
