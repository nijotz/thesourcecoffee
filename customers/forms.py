from django_localflavor_us import forms
from django.forms import ModelForm
from mezzanine.accounts.forms import ProfileForm
from customers.models import Address


class AddressForm(ModelForm):

    class Meta:
        model = Address

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['zipcode'] = forms.USZipCodeField()


class CustomerForm(ProfileForm):

    def save(self, *args, **kwargs):
        user = super(CustomerForm, self).save(*args, **kwargs)
        return user
