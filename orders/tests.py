from datetime import date, timedelta
from mock import patch
from django.core.urlresolvers import reverse
from django.test import Client
from customers.tests import CustomerTestCase
from orders.models import Order

class OrderTestCase(CustomerTestCase):


    def setUp(self):
        super(OrderTestCase, self).setUp()


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
        url = reverse('admin:admin_orders_fulfillment')

        # mock up order date to pretend it's 30 days in the future
        future = date.today() + timedelta(days=30)
        class fakedate(date):
            @classmethod
            def today(cls):
                return future
        patcher = patch('orders.views.date', fakedate)
        patcher.start()

        # login as the admin user and get the orders to be fulfilled
        client.login(username='admin', password='default')
        response = client.get(url)
        patcher.stop()

        # fulfill the first order
        order = response.context['orders'][0]
        post = {'order_id': order.id, 'tracking_number': 123123123123123}

        # verify
        response = client.post(url, post)
        self.assertEqual(response.status_code, 200)
