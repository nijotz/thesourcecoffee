from django.db import models


class GiftSubscription(models.Model):
    gifter = models.ForeignKey('customers.Customer', related_name='gifted_')
    giftee
    plan
    code
    redeemed
