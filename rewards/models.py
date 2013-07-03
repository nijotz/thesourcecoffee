from customers.models import Customer
from django.db import models
from orders.models import Order
from hashlib import md5
from rewards.utils import base62encode

# This is so we don't get stupid hashes like 'b' intially.
CUSTOMER_PK_OFFSET = 10000000

class Reward(models.Model):
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    rewardee = models.ForeignKey(Customer, related_name="rewardee_set")
    invitee = models.ForeignKey(Customer, related_name="invitee_set")
    order = models.ForeignKey(Order, null=True)

    def __unicode__(self):
        return unicode(self.order)

class InviteCode(models.Model):
    customer = models.OneToOneField(Customer, related_name="+",
        null=False)
    code = models.CharField(max_length=10, null=False)

    def save(self, *args, **kwargs):
        if self.code is None or self.code == u'':
            num = self.customer.pk + CUSTOMER_PK_OFFSET
            self.code = base62encode(num)
        super(InviteCode, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.code)
