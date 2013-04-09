from django.forms.models import inlineformset_factory
from django.forms.widgets import TextInput
from django_localflavor_us import forms
from mezzanine.accounts.forms import ProfileForm
from customers.models import Customer
from subscriptions.models import Subscription

class CustomerForm(ProfileForm):

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['code'] = forms.USZipCodeField()
    
    def save(self, *args, **kwargs):
        user = super(CustomerForm, self).save(*args, **kwargs)
        return user.customer
