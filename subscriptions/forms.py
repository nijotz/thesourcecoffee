from django import forms
from subscriptions.models import CustomerSubscription, Subscription

class CustomerSubscriptionForm(forms.ModelForm):
    #subscription = forms.ModelChoiceField(
    #    queryset=Subscription.objects.filter(active=True, public=True))

    class Meta:
        model = CustomerSubscription
        fields = ('subscription', 'location')
