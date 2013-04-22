from customers.tests import CustomerTestCase

class SubscriptionTestCase(CustomerTestCase):


    def setUp(self):
        super(SubscriptionTestCase, self).setUp()


    def test_subscription_is_required_on_signup(self):

        post = {
            'plan': None,
            'email': 'testuser1@example.com'
        }
        (response, post) = self.base_sign_up(post)

        errors = response.context['subscription_form'].errors
        self.assertIn('plan', errors.keys())
