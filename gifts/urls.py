from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^check_code$', 'gifts.views.check_code', name="gifts_check_code"),
    url(r'^purchased$', 'gifts.views.purchased', name="gifts_purchased"),
)
