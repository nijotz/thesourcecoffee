from datetime import date, datetime, timedelta
from django.db import models
import stripe
from base.models import SiteSetting, StripeObject


class LocationFullException(Exception):
    pass


class Plan(StripeObject):
    amount = models.FloatField()
    price = models.DecimalField(decimal_places=2, max_digits=7)
    public = models.BooleanField(default=True)
    interval = models.IntegerField()

    class Meta:
        unique_together = ('amount', 'price', 'interval')

    def __unicode__(self):
        if self.amount < 1:
            amount = self.amount * 16
            unit = 'ozs'
        else:
            amount = self.amount
            unit = 'lbs'

        return '{amount:g} {unit} every {interval} month(s) for ${price:,.2f}'\
            .format(
                amount=amount,
                unit=unit,
                interval=self.interval,
                price=self.price)

    def save(self, *args, **kwargs):

        # dynamic default for interval
        self.interval = SiteSetting.objects.get(key='subscriptions.length').value

        # sync with stripe
        if self.stripe_id != str(self):
            try:
                plan = stripe.Plan.retrieve(str(self))
                plan.delete()
            except stripe.InvalidRequestError:
                pass

            self.stripe_id = str(self)

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


class Subscription(models.Model):
    customer = models.OneToOneField('customers.Customer', related_name="subscription", null=True)
    plan = models.ForeignKey('subscriptions.Plan', related_name='subscriptions')
    location = models.ForeignKey('locations.Location', related_name='subscriptions')

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

        # make sure location is not full
        if self.location.capacity_remaining < self.plan.amount:
            raise LocationFullException

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
