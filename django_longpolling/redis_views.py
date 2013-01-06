from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import logging
import redis
from .views import BaseLongPollingView


logger = logging.getLogger(__name__)


redis_connection_pool = redis.ConnectionPool(
    **getattr(settings, 'REDIS_PUBSUB_CONFIGS', {})
)


class BaseRedisPubSubView(BaseLongPollingView):
    redis_channel = None

    def iterator(self):
        connection = redis.Redis(connection_pool=redis_connection_pool)
        pubsub = connection.pubsub()
        pubsub.subscribe(self.get_redis_channel())
        for message in pubsub.listen():
            if message['type'] == 'message':
                try:
                    self.write(self.decode_message(message['data']))
                except Exception, e:
                    logger.exception(e)
                finally:
                    break
        pubsub.unsubscribe()
        self.close_connection()

    def get_redis_channel(self):
        """
        get channel from url
        url(r'^/(?P<channel>\w+)/$', BaseRedisPubSubView.as_view())

        get channel from as_view method
        url(r'^/$', BaseRedisPubSubView.as_view(redis_channel="foo"))

        """
        if self.kwargs.get('channel'):
            return self.kwargs['channel']
        elif hasattr(self, 'redis_channel'):
            return self.redis_channel
        else:
            raise ImproperlyConfigured("redis channel name is missing")

    def decode_message(self, message):
        """
        override this method if decoding of the message
        from redis to http response is needed
        """
        return message


class RedisUserPubSubView(BaseRedisPubSubView):
    """
    same as RedisPubSubView but uses user attributes
    to make the pub sub channel name

    eg.
    url(r'^/$', RedisUserPubSubView.as_view(redis_channel="feed:{0.pk}"))
    """

    redis_channel = None

    def get_redis_channel(self):
        if self.redis_channel is None:
            raise ImproperlyConfigured("\
                you should send this class the `redis_channel` param")
        return self.redis_channel.format(self.request.user)
