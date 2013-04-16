from django.conf.urls import patterns, url
import orders.views


def get_admin_site(BaseAdminSite):

    class AdminSite(BaseAdminSite):

        def get_urls(self, *args, **kwargs):

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
            )
            return urlpatterns

    return AdminSite()
