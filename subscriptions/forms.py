from django.forms import ModelForm
from subscriptions.models import CustomerSubscription

class CustomerSubscriptionForm(ModelForm):
    class Meta:
        model = CustomerSubscription
