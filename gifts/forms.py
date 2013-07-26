from django import forms
from gifts.models import GiftSubscription

class GiftSubscriptionForm(forms.Form):
    gifter = forms.EmailField(label="Your e-mail")
    giftee = forms.EmailField(label="Recipient's e-mail")
