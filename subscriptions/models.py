from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class SubscriptionType(models.Model):

    def __unicode__(self):
        return '%d oz. every %d days' % (self.amount, self.period)

    amount = models.FloatField()
    period = models.IntegerField()


class Subscription(models.Model):

    def __unicode__(self):
        return '%d oz. of %s every %d days' % (
            self.subscription_type.amount,
            str(self.product),
            self.subscription_type.period
        )

    subscription_type = models.ForeignKey(SubscriptionType)
    product = models.ForeignKey(Product)
    price = models.FloatField()


class CustomerSubscription(models.Model):
    customer = models.ForeignKey(User)
    subscription = models.ForeignKey(Subscription)
