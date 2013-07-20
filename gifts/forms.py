from django import forms
from gifts.models import GiftSubscription

class GiftSubscriptionForm(forms.Form):
    gifter = forms.EmailField()
    giftee = forms.EmailField()
