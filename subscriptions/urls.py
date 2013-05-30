from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'subscriptions.views.index', name='subscription'),
    url(r'^update$', 'subscriptions.views.update', name='subscription_update'),
)
