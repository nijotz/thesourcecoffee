from datetime import date, datetime, timedelta
from django.db import models
from customers.models import Customer
from locations.models import Location
from base.models import SiteSetting


class Plan(models.Model):
    amount = models.FloatField()
    price = models.DecimalField(decimal_places=2, max_digits=7)
    public = models.BooleanField(default=True)

    def __unicode__(self):
        if self.amount < 1:
            return '{} ozs - ${:,.2f}'.format(self.amount * 16, self.price)
        else:
            return '{} lbs - ${:,.2f}'.format(self.amount, self.price)

    @property
    def stripe_id(self):
        return str(self)


class Subscription(models.Model):
    customer = models.OneToOneField(Customer, related_name="subscription", null=True)
    plan = models.ForeignKey(Plan, related_name='subscriptions')
    location = models.ForeignKey(Location, related_name='subscriptions')

    # stripe fields
    started = models.DateTimeField()
    canceled = models.DateTimeField(null=True)
    ended = models.DateTimeField(null=True)
    current_period_start = models.DateTimeField(null=True)
    current_period_end = models.DateTimeField(null=True)
    status = models.CharField(max_length=25)  # trialing, active, past_due, canceled, or unpaid

    def __unicode__(self):
        return '%s - %s' % (self.customer, self.subscription)

    @property
    def period_is_current(self):
        return self.current_period_end > datetime.utcnow()

    @property
    def status_is_current(self):
        return self.status in ["trialing", "active", "canceled"]

    @property
    def active(self):
        return self.period_is_current and self.status_is_current

    def save(self):
        if not self.id:
            subscription_length = SiteSetting.objects.get(
                key='subscription.length').value
            self.expiration_date = date.today() + timedelta(days=subscription_length)
            super(CustomerSubscription, self).save()
