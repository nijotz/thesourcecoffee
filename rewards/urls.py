from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'rewards.views.home', name="rewards_home"),
)
