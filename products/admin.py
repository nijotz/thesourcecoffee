from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from products.models import Product

admin.site.register(Product, PageAdmin)
