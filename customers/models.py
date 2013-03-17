from django.contrib.auth.models import User
from django.db import models
from django_localflavor_us.models import PhoneNumberField
from south.modelsinspector import add_introspection_rules


# South needs to know about the PhoneNumberField
add_introspection_rules([], ["^django_localflavor_us\.models\.PhoneNumberField"])


class Customer(models.Model):
    user = models.OneToOneField(User)
    phone = PhoneNumberField()

    def __unicode__(self):
        return self.user.email
