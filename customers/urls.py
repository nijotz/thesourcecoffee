from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^signup/$', 'customers.views.signup', name="customers_signup"),
    url(r'^$', 'customers.views.home', name="customers_home"),
)
