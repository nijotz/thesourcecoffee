from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django_localflavor_us.models import PhoneNumberField
from south.modelsinspector import add_introspection_rules
import stripe
from locations.models import Area

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = getattr(settings, "STRIPE_API_VERSION", "2012-11-07")

# South needs to know about the PhoneNumberField
add_introspection_rules([], ["^django_localflavor_us\.models\.PhoneNumberField"])


class StripeObject(models.Model):
    
    stripe_id = models.CharField(max_length=50, unique=True)
    
    class Meta:
        abstract = True


class Customer(StripeObject):
    
    user = models.OneToOneField(User)
    phone = PhoneNumberField()
    area = models.ForeignKey(Area, null=True)

    card_fingerprint = models.CharField(max_length=200, blank=True)
    card_last_4 = models.CharField(max_length=4, blank=True)
    card_kind = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        if not self.stripe_id:
            customer = stripe.Customer.create(email=self.user.email)
            self.stripe_id = customer.id
        super(Customer, self).save(*args, **kwargs)

    @property
    def stripe_customer(self):
        return stripe.Customer.retrieve(self.stripe_id)

    def update_card(self, token):
        sc = self.stripe_customer
        sc.card = token
        sc.save()
        self.card_fingerprint = sc.active_card.fingerprint
        self.card_last_4 = sc.active_card.last4
        self.card_kind = sc.active_card.type
        self.save()

    def subscribe(self, plan):
        sc = self.stripe_customer
        resp = sc.update_subscription(plan=plan.stripe_id)
        self.sync_subscription()
        self.send_invoice()

    def sync_subscription(self):
        stripe_sub = self.stripe_customer.subscription
        if stripe_sub:
            try:
                sub = self.subscription
                sub.plan = Plan.objects.get(id=stripe_sub.plan.stripe_id)
                sub.current_period_start = convert_tstamp(stripe_sub.current_period_start)
                sub.current_period_end = convert_tstamp(stripe_sub.current_period_end)
                sub.amount = (stipe_sub.plan.amount / 100.0)
                sub.status = stipe_sub.status
                sub.start = convert_tstamp(stipe_sub.start)
                sub.quantity = stipe_sub.quantity
                sub.save()
            except Subscription.DoesNotExist:
                sub = Subscription.objects.create(
                    customer=self,
                    plan=Plan.objects.get(id=stripe_sub.plan.stripe_id),
                    current_period_start=convert_tstamp(stripe_sub.current_period_start),
                    current_period_end=convert_tstamp(stripe_sub.current_period_end),
                    amount=(stripe_sub.plan.amount / 100.0),
                    status=stripe_sub.status,
                    start=convert_tstamp(stripe_sub.start),
                    quantity=stripe_sub.quantity
                )

            if stripe_sub.trial_start and stripe_sub.trial_end:
                sub.trial_start = convert_tstamp(stripe_sub.trial_start)
                sub.trial_end = convert_tstamp(stripe_sub.trial_end)
                sub.save()

            return sub

    def send_invoice(self):
        try:
            invoice = stripe.Invoice.create(customer=self.stripe_id)
            invoice.pay()
            return True
        except stripe.InvalidRequestError:
            return False  # There was nothing to invoice
