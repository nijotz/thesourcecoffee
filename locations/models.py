from datetime import datetime
from django.db import models
from base.models import SiteSetting


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

    @property
    def capacity(self):
        "alias for capacity_total"
        return self.capacity_total

    @property
    def capacity_total(self):
        return SiteSetting.objects.get(key='locations.capacity').value

    @property
    def capacity_allocated(self):
        return (self.subscriptions
            .filter(current_period_end__gt=datetime.now())
            .aggregate(models.Sum('plan__amount'))
            .values()[0]) or 0

    @property
    def capacity_remaining(self):
        return self.capacity_total - self.capacity_allocated
