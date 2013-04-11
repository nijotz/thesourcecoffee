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
    fixtures = ['base/fixtures/site_settings.json']


    def setUp(self):
        super(SubscriptionTestCase, self).setUp()

        self.area = Area.objects.create(name='Test Area')
        self.plan = Plan.objects.create(amount=3, price=20.00)
        self.location = Location.objects.create(area=self.area, address='Test')

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
        profile_form = get_profile_form()
        self.customer = profile_form(post).save()

        token = stripe.Token.create(
            card={
                'number': '4242424242424242',
                'exp_month': '12',
                'exp_year': datetime.now().year + 1,
                'cvc': '123',
            })
        self.customer.update_card(token.id)


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
        sub = Subscription(plan=self.plan, customer=self.customer)
        sub.save()
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
            'plan': self.plan.id,
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
        self.assertEqual(response.status_code, 302)
