from django.db import models
from promotions.models import Code


class GiftSubscription(models.Model):
    gifter = models.EmailField(max_length=254)
    giftee = models.EmailField(max_length=254)
    plan = models.ForeignKey('subscriptions.Plan')
    code = models.ForeignKey('promotions.Code')
    redeemed = models.DateTimeField(null=True, default=None)

    def save(self, *args, **kwargs):
        try:
            self.code
        except Code.DoesNotExist:
            code = Code()
            code.save()
            self.code = code

        super(GiftSubscription, self).save(*args, **kwargs)
