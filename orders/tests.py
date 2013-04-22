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
