from django.db import models


class Area(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Location(models.Model):
    area = models.ForeignKey(Area)
    address = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.address
