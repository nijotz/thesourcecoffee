from base.models import StripeObject
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django_localflavor_us.models import PhoneNumberField, USStateField, USPostalCodeField
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = getattr(settings, "STRIPE_API_VERSION", "2012-11-07")

# South needs to know about the PhoneNumberField and USSateField
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^django_localflavor_us\.models\.PhoneNumberField"])
add_introspection_rules([], ["^django_localflavor_us\.models\.USStateField"])


class Customer(StripeObject):

    user = models.OneToOneField(User)
    phone = PhoneNumberField()
    street = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    state = USStateField()
    zipcode = models.CharField(max_length=10)
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

    def invite_code(self):
        # Avoid circular import
        from rewards.models import InviteCode
        code = InviteCode.objects.filter(customer=self)
        if code.exists():
            return code.get()

        return InviteCode.objects.create(customer=self)

    def grant_reward(self, invitee):
        from subscriptions.models import Subscription
        from rewards.models import Reward
        from orders.models import Order
        try:
            invitee_subscription = invitee.subscription
            plan = self.subscription.plan
        except Subscription.DoesNotExist, e:
            # Either this customer doesn't have a plan or the invtee
            # doen't have one.
            return None

        try:
            already_invited = invitee.reward_resulting_from_my_invitation
        except Reward.DoesNotExist, e:
            pass
        else:
            return 'Already invited.' # This person was already invited.

        if plan.interval > 1:
            # The invitee probably signed up for 3 months or a year. Hooray,
            # then the customer gets a reward right away!
            order = Order.objects.create(subscription=self.subscription,
                to_be_fulfilled=datetime.now()) #TODO: Remove to_be_fulfilled from here
            return Reward.objects.create(rewardee=self, invitee=invitee,
                order=order)
        elif plan.interval == 1:
            # They're on a month-to-month plan and need to be treated a bit
            # differently. If this customer has at least a month of orders
            # then we can credit them right away.
            return Reward.objects.create(rewardee=self, invitee=invitee,
                order=None)

        # Something weird happened.
        return None


    def update_card(self, token):
        sc = self.stripe_customer
        sc.card = token
        sc.save()
        self.card_fingerprint = sc.active_card.fingerprint
        self.card_last_4 = sc.active_card.last4
        self.card_kind = sc.active_card.type
        self.save()
