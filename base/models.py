from json_field import JSONField
from django.db import models

class SiteSetting(models.Model):
    value = JSONField()
    key = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=1024)

    def __unicode__(self):
        return self.key


class StripeObject(models.Model):

    stripe_id = models.CharField(max_length=50, unique=True)

    class Meta:
        abstract = True
