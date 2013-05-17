from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^signup$', 'customers.views.signup', name="signup"),
    url(r'^$', 'customers.views.home', name="account_home"),
)
