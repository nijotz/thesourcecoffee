from base.models import SiteSetting
from customers.tests import CustomerTestCase
from subscriptions.models import LocationFullException, Subscription

class LocationTestCase(CustomerTestCase):


    def setUp(self):
        super(LocationTestCase, self).setUp()


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
