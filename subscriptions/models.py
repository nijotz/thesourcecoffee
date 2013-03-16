from django.db import models
from customers.models import Customer
from locations.models import Location


class Subscription(models.Model):
    amount = models.FloatField()
    active = models.BooleanField(default=True)
    public = models.BooleanField(default=True)

    def __unicode__(self):
        if self.amount < 1:
            return '%d ozs' % (self.amount * 16)
        else:
            return '%d lbs' % (self.amount)


# A manual many-to-many with a unique is an oxymoron. However, I can definitely
# forsee many CustSub object for a history of what their subscription has been
# or having more than one subscription to subscribe to.
class CustomerSubscription(models.Model):
    customer = models.ForeignKey(Customer, related_name='subscriptions')
    subscription = models.ForeignKey(Subscription)
    location = models.ForeignKey(Location, related_name='subscriptions')

    class Meta:
        unique_together = ('customer', 'subscription')
