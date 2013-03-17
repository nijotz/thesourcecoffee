from datetime import date, timedelta
from django.db import models
from customers.models import Customer
from locations.models import Location
from base.models import SiteSetting


class Subscription(models.Model):
    amount = models.FloatField()
    public = models.BooleanField(default=True)

    def __unicode__(self):
        if self.amount < 1:
            return '%d ozs' % (self.amount * 16)
        else:
            return '%d lbs' % (self.amount)


# This is to keep logic related to active subscriptions in one place
class CustomerSubscriptionManager(models.Manager):

    def active(self):
        try:
            return self.get_query_set().get(
                expiration_date__gt=date.today(),
                activation_date__lte=date.today())
        except CustomerSubscription.DoesNotExist:
            return None


class CustomerSubscription(models.Model):
    customer = models.ForeignKey(Customer, related_name='subscriptions')
    subscription = models.ForeignKey(Subscription, related_name='customer_subscriptions')
    location = models.ForeignKey(Location, related_name='subscriptions')
    activation_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField()

    objects = CustomerSubscriptionManager()

    class Meta:
        unique_together = ('customer', 'subscription')

    def __unicode__(self):
        return '%s - %s' % (self.customer, self.subscription)

    @property
    def active(self):
        return self.expiration_date > date.today() and \
            self.activation_date <= date.today()

    def save(self):
        if not self.id:
            subscription_length = SiteSetting.objects.get(
                key='subscription.length').value
            self.expiration_date = date.today() + timedelta(days=subscription_length)
            super(CustomerSubscription, self).save()
