from django import forms
from subscriptions.models import Plan, Subscription


PLAN_AMOUNT_CHOICES = (
    (0.125, '2oz Trial'),
    (0.5, '8oz'),
    (0.75, '12oz'),
    (1.0, '16oz'),
)

PLAN_INTERVAL_CHOICES = (
    (1, 'Monthly'),
    (3, '3 months'),
    (12, '1 year'),
)

class SubscriptionForm(forms.Form):

    amount = forms.ChoiceField(
        widget=forms.widgets.RadioSelect,
        choices=PLAN_AMOUNT_CHOICES)
    interval = forms.ChoiceField(
        widget=forms.widgets.RadioSelect,
        choices=PLAN_INTERVAL_CHOICES)
