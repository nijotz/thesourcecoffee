from functools import update_wrapper
from django.conf.urls import patterns, url
import customers.views
import orders.views


def get_admin_site(BaseAdminSite):

    class AdminSite(BaseAdminSite):

        def get_urls(self, *args, **kwargs):

            def wrap(view, cacheable=False):
                def wrapper(*args, **kwargs):
                    return self.admin_view(view, cacheable)(*args, **kwargs)
                return update_wrapper(wrapper, view)

            urlpatterns = super(AdminSite, self).get_urls(*args, **kwargs)
            urlpatterns += patterns('',
                url(r'^orders/fulfillment/$',
                    self.admin_view(orders.views.fulfillment),
                    name='admin_orders_fulfillment',
                ),
                url(r'^orders/fulfillment/mailing_stickers',
                    self.admin_view(orders.views.mailing_stickers),
                    name='admin_orders_mailing_stickers',
                ),
                url(r'^functions/add_test_customer',
                    self.admin_view(customers.views.add_test_customer),
                    name='admin_add_test_customer',
                ),
                url(r'^functions/move_orders_back',
                    self.admin_view(orders.views.move_orders_back),
                    name='admin_move_orders_back',
                ),
            )

            return urlpatterns

    return AdminSite()
