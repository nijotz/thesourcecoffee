from datetime import datetime
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from mezzanine.accounts import get_profile_form
import stripe
import base
from base.models import SiteSetting
from customers.models import Customer
from locations.models import Area, Location
from orders.models import Order
from subscriptions.models import Plan, Subscription, LocationFullException


class SubscriptionTestCase(TestCase):
    fixtures = [
        'base/fixtures/site_settings.json',
        'subscriptions/fixtures/subscriptions.json',]


    def setUp(self):

        super(SubscriptionTestCase, self).setUp()

        self.plan = Plan.objects.all()[0]

        # Sign up a user to be used for other tests
        post = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'TestUser',
            'email': 'testuser@example.com',
            'password1': 'testpass',
            'password2': 'testpass',
            'phone': '555-555-5555',
            'street': '123 Easy St',
            'city': 'City',
            'state': 'TX',
            'code': '12345',
            'plan': self.plan.id,
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
        response = client.post(reverse('signup'), post)
        self.assertEqual(response.status_code, 302)

        self.customer = Customer.objects.all()[0]
        self.customer.password_text = post['password1']


    def test_location_capacity(self):
        return # location capacity will be implemented later
        capacity_setting = SiteSetting.objects.get(key='locations.capacity')
        orig_capacity = capacity_setting.value
        capacity_setting.value = 1
        capacity_setting.save()

        with self.assertRaises(LocationFullException):
            while True:
                Subscription.objects.create(
                    customer=self.customer,
                    location=self.location,
                    plan=self.plan)

        capacity_setting.value = orig_capacity
        capacity_setting.save()


    def test_orders_are_created(self):
        sub = self.customer.subscription
        self.assertTrue(len(Order.objects.filter(subscription=sub)) > 0)


    def test_subscription_is_required_on_signup(self):
        post = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'TestUser1',
            'email': 'testuser1@example.com',
            'password1': 'testpass',
            'password2': 'testpass',
            'phone': '555-555-5555',
            'street': '123 Easy St',
            'city': 'City',
            'state': 'TX',
            'code': '12345',
        }

        token = stripe.Token.create(
            card={
                'number': '4242424242424242',
                'exp_month': '12',
                'exp_year': datetime.now().year + 1,
                'cvc': '123',
            })
        post['token'] = token.id

        client = Client()
        response = client.post(reverse('signup'), post)

        errors = response.context['subscription_form'].errors
        self.assertIn('plan', errors.keys())

        required = False
        for error in errors['plan']:
            if 'required' in error:
                required = True
                break

        self.assertEqual(required, True)


    def test_order_list(self):
        client = Client()
        post = {
            'username': self.customer.user.username,
            'password': self.customer.password_text
        }
        client.post(reverse('login'), post)
        response = client.get(reverse('orders_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['orders']) > 0)
