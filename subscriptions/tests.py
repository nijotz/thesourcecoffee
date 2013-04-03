from django.test import TestCase
from mezzanine.accounts import get_profile_form
from base.models import SiteSetting
from customers.models import Customer
from locations.models import Area, Location
from subscriptions.models import Plan, Subscription, LocationFullException


class SubscriptionTestCase(TestCase):

    def setUp(self):
        super(SubscriptionTestCase, self).setUp()

        SiteSetting.objects.create(key='subscriptions.length', value=3)
        SiteSetting.objects.create(key='locations.capacity', value=100)
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
