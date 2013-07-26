from base.models import StripeObject, SiteSetting
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django_localflavor_us.models import PhoneNumberField, USStateField, USPostalCodeField
from subscriptions.models import Subscription
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
        from rewards.models import Reward
        from orders.models import Order
        try:
            subscription = self.subscription
            if subscription is not None:
                plan = subscription.plan
            else:
                return None
        except Subscription.DoesNotExist, e:
            # NO PLAN
            return None

        try:
            already_invited = invitee.reward_resulting_from_my_invitation
        except Reward.DoesNotExist, e:
            pass
        else:
            return 'Already invited.' # This person was already invited.

        # Not month to month
        if plan.interval > 1:
<<<<<<< HEAD
=======
            # The invitee probably signed up for 3 months or a year. Hooray,
            # then the customer gets a reward right away!
            interval = SiteSetting.objects.get(key='subscriptions.interval').value
            last_order = self.orders.all().order_by('-to_be_fulfilled')[0]
            to_be_fulfilled = last_order.to_be_fulfilled + timedelta(weeks=interval)
>>>>>>> origin/master
            order = Order.objects.create(subscription=self.subscription,
                to_be_fulfilled=to_be_fulfilled)
            return Reward.objects.create(rewardee=self, invitee=invitee,
                order=order)
        elif plan.interval == 1:
            # See if the rewardee has at least a month of orders
            if self.has_enough_orders_for_m2m_reward:
                order = Order.objects.create(subscription=self.subscription,
                    to_be_fulfilled=datetime.now()) #TODO: Remove to_be_fulfilled from here
                return Reward.objects.create(rewardee=self, invitee=invitee,
                    order=order)

            return Reward.objects.create(rewardee=self, invitee=invitee,
                order=None)

        # Something weird happened.
        return None

    def make_sure_rewards_have_orders(self):
        '''
        This function is called during fulfillment to see if this customer
        needs to have any rewards updated because they are month to month.
        See github issue 4 for more information.
        '''
        from orders.models import Order
        rewards_without_orders = self.rewards.filter(order__isnull=True)

        if (rewards_without_orders.exists()
            and self.has_enough_orders_for_m2m_reward):
            try:
                sub = self.subscription
            except:
                pass
            else:
                # If they're eligible, we should create orders for all of
                # their rewards.
                for reward in rewards_without_orders:
                    order = Order.objects.create(subscription=sub,
                        to_be_fulfilled=datetime.now()) #TODO: Remove to_be_fulfilled from here
                    reward.order = order
                    reward.save()

    @property
    def is_month_to_month(self):
        try:
            plan = self.subscription.plan
        except:
            return False

        if plan.interval == 1:
            return True

        return False

    @property
    def has_enough_orders_for_m2m_reward(self):
        assert False == 'TODO'

    def update_card(self, token):
        sc = self.stripe_customer
        sc.card = token
        sc.save()
        self.card_fingerprint = sc.active_card.fingerprint
        self.card_last_4 = sc.active_card.last4
        self.card_kind = sc.active_card.type
        self.save()

    @property
    def subscription(self):
        try:
            return self._subscription
        except Subscription.DoesNotExist:
            return None
