from django.conf.urls.defaults import *
from django_longpolling.redis_views import BaseRedisPubSubView
from django_longpolling.redis_views import RedisUserPubSubView


urlpatterns = patterns('',
    url(r'^sub/$', BaseRedisPubSubView.as_view(redis_channel="default_channel")),
    url(r'^sub/(?P<channel>\w+)/$', BaseRedisPubSubView.as_view()),
    url(r'^userfeed/$', RedisUserPubSubView.as_view(redis_channel="feed:{0.pk}")),
)
