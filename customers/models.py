from django.contrib.auth.models import User
from django.db import models
from django_localflavor_us.models import PhoneNumberField

class Customer(models.Model):
    user = models.OneToOneField(User)
    phone = PhoneNumberField()

    def __unicode__(self):
        return self.user.email
