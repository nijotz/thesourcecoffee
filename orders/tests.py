from datetime import date, timedelta
from mock import patch
from django.core.urlresolvers import reverse
from django.test import Client
from base.models import SiteSetting
from customers.tests import CustomerTestCase, signup_test_customer
from orders.models import Order


class OrderTestCase(CustomerTestCase):

    def setUp(self):
        super(OrderTestCase, self).setUp()
        self.fulfillment_url = reverse('admin:admin_orders_fulfillment')

        # mock up order date to pretend it's 30 days in the future
        future = date.today() + timedelta(days=30)

        class fakedate(date):
            @classmethod
            def today(cls):
                return future

        self.future_patcher = patch('orders.views.date', fakedate)

    def test_orders_are_created(self):
        sub = self.customer.subscription
        self.assertTrue(len(Order.objects.filter(subscription=sub)) > 0)

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

    def test_order_fulfillment(self):
        client = Client()

        # login as the admin user and get the orders to be fulfilled
        self.future_patcher.start()
        client.login(username='admin', password='default')
        response = client.get(self.fulfillment_url)
        self.future_patcher.stop()

        # fulfill the first order
        order = response.context['orders'][0]
        post = {'order_id': order.id, 'tracking_number': 123123123123123}

        # verify
        response = client.post(self.fulfillment_url, post)
        self.assertEqual(response.status_code, 200)

    def test_order_fulfillment_limit(self):

        # create lots of orders to be fulfilled
        for i in range(0, 5):
            signup_test_customer()

        # set the limit really low
        maximum = SiteSetting.objects.get(key='orders.max_fulfillment_day')
        maximum.value = 1
        maximum.save()

        # make sure there are orders to be fulfilled that aren't listed
        self.future_patcher.start()
        unfilled_orders = Order.objects.filter(
            to_be_fulfilled__lte=date.today() + timedelta(days=30),  # Magic numbers... matches the 30 in setUp
            fulfilled=None)
        self.client.login(username='admin', password='default')
        response = self.client.get(self.fulfillment_url)
        self.future_patcher.stop()

        self.assertTrue(len(unfilled_orders) > len(response.context['orders']))
