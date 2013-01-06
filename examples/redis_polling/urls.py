from django.conf.urls.defaults import *
from django_longpolling.redis_views import BaseRedisPubSubView
from django_longpolling.redis_views import RedisUserPubSubView


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^admin/', include(admin.site.urls)),
    url(r'sub/$', BaseRedisPubSubView.as_view(redis_channel="default_channel", timeout=15)),
    url(r'^sub/(?P<channel>\w+)/$', BaseRedisPubSubView.as_view()),
    url(r'^userfeed/$', RedisUserPubSubView.as_view(redis_channel="feed:{0.pk}")),
    # (r'^redis_polling/', include('redis_polling.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
)
