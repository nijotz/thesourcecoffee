from json_field import JSONField
from django.db import models

class SiteSetting(models.Model):
    value = JSONField()
    key = models.CharField(max_length=256)
    description = models.CharField(max_length=1024)

    def __unicode__(self):
        return self.key
