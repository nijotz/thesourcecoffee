from django import forms
from django.db.models import Q
from subscriptions.models import CustomerSubscription, Subscription

class CustomerSubscriptionForm(forms.ModelForm):
    #subscription = forms.ModelChoiceField(
    #    queryset=Subscription.objects.filter(active=True, public=True))

    def __init__(self, customer, *args, **kwargs):
        super(CustomerSubscriptionForm, self).__init__(*args, **kwargs)
        queryset = Subscription.objects.filter(
            Q(customer_subscriptions__customer=customer) |
            Q(public=True) )
        self.fields['subscription'].queryset = queryset

    class Meta:
        model = CustomerSubscription
        fields = ('subscription', 'location')
