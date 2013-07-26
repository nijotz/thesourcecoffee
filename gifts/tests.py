from datetime import datetime
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
import stripe
from gifts.models import GiftSubscription
from subscriptions.models import Plan


class GiftSubscriptionTest(TestCase):
    fixtures = ['subscriptions/fixtures/subscriptions.json',]

    def test_gift_signup(self):
        plan = Plan.objects.all()[0]

        post = {
            'gift': 'on',
            'gifter': 'test1@example.com',
            'giftee': 'test2@example.com',
            'amount': plan.amount,
            'interval': plan.interval,
        }

        token = stripe.Token.create(
            card={
                'number': '4242424242424242',
                'exp_month': '12',
                'exp_year': datetime.now().year + 1,
                'cvc': '123',
            })

        post['stripeToken'] = token.id

        client = Client()
        response = client.post(reverse('customers_signup'), post)

        gifts = GiftSubscription.objects.filter(gifter=post['gifter']).count()
        self.assertNotEqual(gifts, 0)
