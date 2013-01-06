DJANGO LONGPOLLING
==================

A long polling implementation for django (1.3+) based on gevent and django
generic class views.

The django_longpolling.views.BaseLongPollingView class implements the basic logic
you have to subclass the iterator method and use the write method to send data
and close_connection to terminate the response.

eg.

    class CountTenView(BaseLongPollingView):

        def iterator(self):
            sleep(10)
            self.write('10!')
            self.close_connection()

and then in your url module:

    url(r'^/count_ten/$', CountTenView.as_view())

This will respond to GET, POST and PUT requests, if you want different handling
of http methods implement the :get, :post, :put methods

By default all long polling requests are timed out with a 200 status code after
:timeout seconds

You can override the timeout with subclassing or sending the new value to the
:as_view method at urls definition time

    url(r'^/count_ten/$', CountTenView.as_view(timeout=10))


Redis pub/sub longpolling
-------------------------
This module comes with a redis pubsub implementation in django_longpolling.redis_views

Subscribe to a channel from url:
    url(r'^/(?P<channel>\w+)/$', BaseRedisPubSubView.as_view())

Subscribe to a static channel:
    url(r'/', BaseRedisPubSubView.as_view(redis_channel="default_channel"))

Subscribe to a user channel:
    url(r'^/$', RedisUserPubSubView.as_view(redis_channel="feed:{0.pk}"))

To support a different channel name logic just subclass one of the two view classes
and then override the :get_redis_channel method to fit that logic.

Redis connection pool parameters can be changed using the REDIS_PUBSUB_CONFIGS setting

eg.
    REDIS_PUBSUB_CONFIGS = {
        'host': '1.2.3.4',
        'port': 1234
    }


Notes about deployment:
I suggest to use some gevent wsgi server as every connection is blocking.
If you use django gunicorn you can run the webserver like this:
    python manage.py run_gunicorn -k 'gevent'

Otherwise have a look at the example django app (wsgi.py and run_wsgi.py)

