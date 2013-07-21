from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'rewards.views.home', name="rewards_home"),
    url(r'^invite_email$', 'rewards.views.invite_email', name="invite_email"),
)
