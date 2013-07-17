from django.contrib import admin
from django.core.urlresolvers import reverse
from customers.models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'user_url',
        'stripe_url',)

    def stripe_url(self, customer):
        return "<a href='https://manage.stripe.com/test/customers/{0}'>{0}</a>".format(
            customer.stripe_id)
    stripe_url.allow_tags = True
    stripe_url.short_description = 'Stripe User'

    def user_url(self, customer):
        return '<a href="{0}?user=">{1}</a>'.format(
            reverse('admin:auth_user_change', args=(customer.user.pk,)),
            customer.user)
    user_url.allow_tags = True
    user_url.short_description = 'User'

admin.site.register(Customer, CustomerAdmin)
