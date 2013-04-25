from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django_localflavor_us.models import PhoneNumberField, USStateField, USPostalCodeField
from south.modelsinspector import add_introspection_rules
import stripe
from base.models import StripeObject

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = getattr(settings, "STRIPE_API_VERSION", "2012-11-07")

# South needs to know about the PhoneNumberField
add_introspection_rules([], ["^django_localflavor_us\.models\.PhoneNumberField"])


class Customer(StripeObject):
    
    user = models.OneToOneField(User)
    phone = PhoneNumberField()
    street = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    state = USStateField()
    code = models.CharField(max_length=10)
    #area = models.ForeignKey('locations.Area', null=True)
    #subscription = models.OneToOneField('subscriptions.Subscription', related_name='customer')

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
