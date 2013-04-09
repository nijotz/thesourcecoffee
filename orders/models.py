from datetime import datetime
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

    def save(self, *args, **kwargs):

        try:
            self.customer
        except Customer.DoesNotExist:
            self.customer = self.subscription.customer

        super(Order, self).save(*args, **kwargs)


class MailOrder(Order):
    tracking_number = models.CharField(max_length=255)
    date_sent = models.DateTimeField()


#class PickupOrder(Order):
#    location = models.ForeignKey(Location)


# When a subscription is created, create all the Order objects for it
@receiver(post_save, sender=Subscription)
def create_subscription_orders(sender, instance, **kwargs):

    num_orders = SiteSetting.objects.get(key='subscriptions.number_of_orders').value
    order_period = ((instance.current_period_end - datetime.now(pytz.utc)) /
        num_orders)

    for i in range(0, num_orders):
        order = Order(
            subscription=instance,
            to_be_fulfilled=datetime.now() + (i * order_period))
        order.save()
