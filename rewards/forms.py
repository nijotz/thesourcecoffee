from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from mezzanine.accounts.forms import ProfileForm

class EmailListForm(forms.Form):
    list_of_emails = forms.CharField(widget=forms.Textarea(attrs={"class": "shadow"}),
        label = "You can also enter friends' email addresses below, separated by a comma to invite them.")

    def clean_list_of_emails(self):
        emails = self.cleaned_data["list_of_emails"]
        emails = emails.replace(" ", "")
        emails = emails.split(",")

        for email in emails:
            try:
                validate_email(email)
            except ValidationError, e:
                raise ValidationError("Not all email addresses were valid.")

        self.cleaned_data["list_of_emails"] = emails

class RewardCodeForm(forms.Form):
    invite_code = forms.CharField(max_length=10,
        label = "Have a reward code?")

