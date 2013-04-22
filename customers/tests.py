from datetime import datetime
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
import stripe
from customers.models import Customer
from subscriptions.models import Plan


class CustomerTestCase(TestCase):
    fixtures = [
        'base/fixtures/site_settings.json',
        'subscriptions/fixtures/subscriptions.json',]

    def base_sign_up(self, custom_post={}):
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
        post.update(custom_post)

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


    def setUp(self, custom_post={}):

        super(CustomerTestCase, self).setUp()

        (response, post) = self.base_sign_up(custom_post)

        self.customer = Customer.objects.get(user__email=post['email'])
        self.customer.password_text = post['password1']

        self.assertEqual(response.status_code, 302)


    def test_signup(self):
        # setUp is signup
        return
