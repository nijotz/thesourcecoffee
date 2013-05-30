from datetime import datetime
from django.db import models
from django.utils import timezone
import stripe
from base.models import SiteSetting, StripeObject


class LocationFullException(Exception):
    pass


def convert_tstamp(response, field_name=None):
    try:
        if field_name and response[field_name]:
            return datetime.fromtimestamp(
                response[field_name],
                timezone.utc
            )
        if not field_name:
            return datetime.fromtimestamp(
                response,
                timezone.utc
            )
    except KeyError:
        pass
    return None


class Plan(StripeObject):
    amount = models.FloatField()
    price = models.DecimalField(decimal_places=2, max_digits=7)
    public = models.BooleanField(default=True)
    interval = models.IntegerField()

    class Meta:
        unique_together = ('amount', 'price', 'interval')

    def __unicode__(self):

        return '{amount_str} for {interval_str} at ${price:,.2f}'\
            .format(
                amount_str=self.amount_str,
                interval_str=self.interval_str,
                price=self.price)

    def save(self, *args, **kwargs):

        # dynamic default for interval
        self.interval = SiteSetting.objects.get(key='subscriptions.length').value

        # dynamic default for stripe_id
        self.stripe_id = str(self)

        # sync with stripe
        try:
            stripe.Plan.retrieve(str(self))
        except stripe.InvalidRequestError:
            stripe.Plan.create(
                amount=int(100 * self.price),
                interval = 'month',
                interval_count=self.interval,
                name=str(self),
                currency='usd',
                id=self.stripe_id)

        super(Plan, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        plan = stripe.Plan.retrieve(self.stripe_id)
        plan.delete()
        super(Plan, self).save(*args, **kwargs)

    @property
    def amount_str(self):
        if self.amount < 1:
            amount = self.amount * 16
            unit = 'ozs'
        else:
            amount = self.amount
            unit = 'lbs'

        if amount == 1:
            unit = unit.rstrip('s')

        return '{amount:g} {unit}'.format(**locals())

    @property
    def interval_str(self):
        interval = self.interval
        unit = 'months'

        if interval == 1:
            unit = unit.rstrip('s')

        return '{interval:g} {unit}'.format(**locals())


class Subscription(models.Model):
    customer = models.OneToOneField('customers.Customer', related_name="subscription")
    plan = models.ForeignKey('subscriptions.Plan', related_name='subscriptions')
    #location = models.ForeignKey('locations.Location', related_name='subscriptions')

    # stripe fields
    started = models.DateTimeField()
    canceled = models.DateTimeField(null=True)
    ended = models.DateTimeField(null=True)
    current_period_start = models.DateTimeField(null=True)
    current_period_end = models.DateTimeField(null=True)
    status = models.CharField(max_length=25)  # trialing, active, past_due, canceled, or unpaid

    def __unicode__(self):
        return '%s - %s' % (self.customer, self.plan)

    def save(self, *args, **kwargs):

        # sync with stripe, this can override every field but customer
        sc = self.customer.stripe_customer
        sc.update_subscription(plan=self.plan.stripe_id)
        stripe_sub = sc.subscription

        if stripe_sub:
            self.plan = Plan.objects.get(stripe_id=stripe_sub.plan.id)
            self.current_period_start = convert_tstamp(stripe_sub.current_period_start)
            self.current_period_end = convert_tstamp(stripe_sub.current_period_end)
            self.status = stripe_sub.status
            self.started = convert_tstamp(stripe_sub.start)

        # make sure location is not full
        #if self.location.capacity_remaining < self.plan.amount:
        #    raise LocationFullException

        super(Subscription, self).save(*args, **kwargs)

    @property
    def period_is_current(self):
        return self.current_period_end > datetime.utcnow()

    @property
    def status_is_current(self):
        return self.status in ["trialing", "active", "canceled"]

    @property
    def active(self):
        return self.period_is_current and self.status_is_current
