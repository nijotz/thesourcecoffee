from django import forms
from django.db.models import Q
from locations.models import Location
from subscriptions.models import Plan, Subscription

class SubscriptionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(SubscriptionForm, self).__init__(*args, **kwargs)

        plans = Plan.objects.filter(public=True)
        self.fields['plan'].queryset = plans

        #locations = Location.objects.filter(area=customer.area)
        #self.fields['location'].queryset = locations

    class Meta:
        model = Subscription
        #fields = ('plan', 'location')
        fields = ('plan',)
