from datetime import datetime
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
import stripe
from customers.models import Customer, signup_test_customer
from subscriptions.models import Plan


class CustomerTestCase(TestCase):
    fixtures = [
        'base/fixtures/site_settings.json',
        'subscriptions/fixtures/subscriptions.json',]

    def setUp(self, custom_data={}):

        super(CustomerTestCase, self).setUp()

        (response, post) = signup_test_customer(custom_data)

        self.customer = Customer.objects.get(user__email=post['email'])
        self.customer.password_text = post['password1']

        self.assertEqual(response.status_code, 302)


    def test_signup(self):
        # setUp is signup
        return
