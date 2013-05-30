from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from customers.models import Customer

admin.site.unregister(User)

class CustomerInline(admin.StackedInline):
    model = Customer

class CustomerAdmin(UserAdmin):
    inlines = [ CustomerInline, ]

admin.site.register(User, CustomerAdmin)
