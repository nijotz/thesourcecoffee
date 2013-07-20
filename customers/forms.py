from django_localflavor_us import forms
from mezzanine.accounts.forms import ProfileForm

class CustomerForm(ProfileForm):

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['zipcode'] = forms.USZipCodeField()
    
    def save(self, *args, **kwargs):
        user = super(CustomerForm, self).save(*args, **kwargs)
        return user
