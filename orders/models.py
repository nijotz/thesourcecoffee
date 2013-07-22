from datetime import datetime, timedelta
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils.managers import InheritanceManager
import pytz
from base.models import SiteSetting
from customers.models import Customer
from locations.models import Location
from subscriptions.models import Subscription


class Order(models.Model):
    customer = models.ForeignKey('customers.Customer', related_name="orders")
    subscription = models.ForeignKey(Subscription)
    to_be_fulfilled = models.DateTimeField()
    fulfilled = models.DateTimeField(null=True)

    # So that objects.all().select_subclassess() returns mail and pickup orders
    #objects = InheritanceManager()

    def __unicode__(self):
        return '{subscription} - {to_be_fulfilled}'.format(
            subscription = self.subscription,
            to_be_fulfilled = self.to_be_fulfilled)

    def fulfill(self, tracking_number):
        self.fulfilled = datetime.now()
        mailorder = MailOrder(order_ptr_id=self.pk)
        mailorder.__dict__.update(self.__dict__)
        mailorder.tracking_number = tracking_number
        mailorder.save()

    def save(self, *args, **kwargs):

        try:
            self.customer
        except Customer.DoesNotExist:
            self.customer = self.subscription.customer

        super(Order, self).save(*args, **kwargs)


class MailOrder(Order):
    tracking_number = models.CharField(max_length=255)


#class PickupOrder(Order):
#    location = models.ForeignKey(Location)


# When a subscription is created, create all the Order objects for it
@receiver(post_save, sender=Subscription)
def create_subscription_orders(sender, instance, **kwargs):

    subscription = instance

    #TODO: this shouldn't be hardcoded; too many magic numbers
    if subscription.interval == 1:
        num_orders = 2
    elif subscription.interval == 3:
        num_orders = 6
    elif subscription.interval == 12:
        num_orders = 26

    for i in range(0, num_orders):
        order = Order(
            subscription=instance,
            to_be_fulfilled=datetime.now() + (i * timedelta(weeks=2))
        order.save()
