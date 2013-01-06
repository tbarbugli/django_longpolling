from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

try:
    from django.http import StreamingHttpResponse as HttpResponse
except ImportError:
    from django.http import HttpResponse

from django.utils.decorators import method_decorator

import gevent
from gevent import event
from gevent import queue
from gevent import sleep


class BaseLongPollingView(View):
    timeout = 30

    def __init__(self, *args, **kwargs):
        super(BaseLongPollingView, self).__init__(*args, **kwargs)
        self.greenlets = []
        self.stream = queue.Queue()
        self.response_completed = event.Event()
        self.spawn(self.cleanup_greenlets)
        self.spawn(self.timeout_ticker, self.timeout)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        handler = super(BaseLongPollingView, self).dispatch(request, *args, **kwargs)
        response = HttpResponse(self._iterator(handler))
        response['Cache-Control'] = 'no-cache'
        return response

    def get(self, request, *args, **kwargs):
        return self.iterator()

    def post(self, request, *args, **kwargs):
        return self.iterator()

    def put(self, request, *args, **kwargs):
        return self.iterator()

    def _iterator(self, handler):
        self.spawn(handler)
        for chunk in self.stream:
            yield chunk

    def cleanup_greenlets(self):
        self.response_completed.wait()
        for g in reversed(self.greenlets):
            g.kill()

    def spawn(self, fn, *args, **kwargs):
        self.greenlets.append(gevent.spawn(fn, *args, **kwargs))

    def close(self):
        self.response_completed.set()

    def close_connection(self):
        self.response_completed.set()
        self.write(StopIteration)

    def timeout_ticker(self, timeout):
        sleep(timeout)
        self.close_connection()

    def write(self, data):
        self.stream.put(data)

    def iterator(self):
        raise NotImplementedError()

