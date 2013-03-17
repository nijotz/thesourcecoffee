from django import forms
from django.db.models import Q
from locations.models import Location
from subscriptions.models import CustomerSubscription, Subscription

class CustomerSubscriptionForm(forms.ModelForm):
    #subscription = forms.ModelChoiceField(
    #    queryset=Subscription.objects.filter(active=True, public=True))

    def __init__(self, customer, *args, **kwargs):

        super(CustomerSubscriptionForm, self).__init__(*args, **kwargs)

        sub_qs = Subscription.objects.filter(
            Q(customer_subscriptions__customer=customer) |
            Q(public=True) )
        self.fields['subscription'].queryset = sub_qs

        loc_qs = Location.objects.filter(area=customer.area)
        self.fields['location'].queryset = loc_qs

    class Meta:
        model = CustomerSubscription
        fields = ('subscription', 'location')
