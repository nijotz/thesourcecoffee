from customers.tests import CustomerTestCase, signup_test_customer

class SubscriptionTestCase(CustomerTestCase):


    def setUp(self):
        super(SubscriptionTestCase, self).setUp()


    def test_subscription_is_required_on_signup(self):

        post = {
            'plan': None,
        }
        (response, post) = signup_test_customer(post)

        errors = response.context['subscription_form'].errors
        self.assertIn('plan', errors.keys())
