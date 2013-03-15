from django.db import models


class Location(models.Model):
    address = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.address
