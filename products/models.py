from django.db import models
from mezzanine.pages.models import Page, RichText


class Product(Page, RichText):

    def __unicode__(self):
        return self.title

    image = models.ImageField(upload_to='products')
