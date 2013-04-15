from django.contrib import admin
from orders.models import Order, MailOrder

admin.site.register(Order)
admin.site.register(MailOrder)
