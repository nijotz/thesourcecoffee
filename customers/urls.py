from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^signup/$', 'customers.views.signup', name="customers_signup"),
    url(r'^tips$', 'customers.views.tips', name="customers_tips"),
    url(r'^$', 'customers.views.home', name="customers_home"),
    url(r'^$', 'customers.views.gifts_sent', name="gifts_sent"),
)
