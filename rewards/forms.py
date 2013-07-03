from django import forms
from mezzanine.accounts.forms import ProfileForm

class RewardCodeForm(forms.Form):
    invite_code = forms.CharField(max_length=10,
        label = "Have a reward code?")

