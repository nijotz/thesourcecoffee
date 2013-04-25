from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.test import Client
from django_localflavor_us.models import PhoneNumberField, USStateField, USPostalCodeField
from south.modelsinspector import add_introspection_rules
import stripe
from base.models import StripeObject
from subscriptions.models import Plan

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


def signup_test_customer(custom_data):
    plan = Plan.objects.all()[0]

    num = Customer.objects.all().count()

    # Sign up a user to be used for other tests
    post = {
        'first_name': 'Test{}',
        'last_name': 'User{}',
        'username': 'TestUser{}',
        'email': 'testuser{}@example.com',
        'password1': 'testpass',
        'password2': 'testpass',
        'phone': '555-555-5555',
        'street': '123 Easy St',
        'city': 'City',
        'state': 'TX',
        'code': '12345',
        'plan': plan.id,
    }

    post.update(custom_data)

    for key in post:
        if type(post[key]) == str:
            post[key] = post[key].format(num + 1)

    token = stripe.Token.create(
        card={
            'number': '4242424242424242',
            'exp_month': '12',
            'exp_year': datetime.now().year + 1,
            'cvc': '123',
        })
    post['stripeToken'] = token.id

    client = Client()
    response = client.post(reverse('signup'), post)

    return (response, post)
