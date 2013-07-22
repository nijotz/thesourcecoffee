from django import forms
from subscriptions.models import Plan, Subscription


PLAN_AMOUNT_CHOICES = (
    (0.125, '2oz Trial'),
    (0.5, '8oz'),
    (0.75, '12oz'),
    (1.0, '16oz'),
)

PLAN_AMOUNT_CHOICES_UPDATE = (
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
        choices=PLAN_INTERVAL_CHOICES, required=False)

    def clean_interval(self):
        interval = self.cleaned_data['interval']
        if self.cleaned_data['amount'] == '0.125':
            if interval:
                raise forms.ValidationError('No interval should be selected for the trial amount')
            else:
                return interval
        else:
            if not interval:
                raise forms.ValidationError('Interval is required')
            else:
                return interval


class SubscriptionUpdateForm(forms.Form):

    amount = forms.ChoiceField(
        widget=forms.widgets.RadioSelect,
        choices=PLAN_AMOUNT_CHOICES_UPDATE)
    interval = forms.ChoiceField(
        widget=forms.widgets.RadioSelect,
        choices=PLAN_INTERVAL_CHOICES)
