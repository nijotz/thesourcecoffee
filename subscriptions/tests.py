from datetime import datetime
from django.test import TestCase
from mezzanine.accounts import get_profile_form
import stripe
from base.models import SiteSetting
from customers.models import Customer
from locations.models import Area, Location
from orders.models import Order
from subscriptions.models import Plan, Subscription, LocationFullException


class SubscriptionTestCase(TestCase):
    fixtures = ['base.site_settings']

    def setUp(self):
        super(SubscriptionTestCase, self).setUp()

        self.area = Area.objects.create(name='Test Area')

        post = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'TestUser',
            'email': 'testuser@example.com',
            'password1': 'testpass',
            'password2': 'testpass',
            'area': 1,
            'phone': '555-555-5555'
        }
        customer_form = get_profile_form()
        form = customer_form(post)
        user = form.save()
        self.customer = user.customer

        token = stripe.Token.create(
            card={
                'number': '4242424242424242',
                'exp_month': '12',
                'exp_year': datetime.now().year + 1,
                'cvc': '123',
            })
        self.customer.update_card(token.id)

        self.location = Location.objects.create(area=self.area, address='Test')
        self.plan = Plan.objects.create(amount=3, price=20.00)

    def test_location_capacity(self):
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
