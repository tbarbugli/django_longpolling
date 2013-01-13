from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

try:
    from django.http import StreamingHttpResponse as HttpResponse
except ImportError:
    from django.http import HttpResponse

from django.utils.decorators import method_decorator

import gevent

class TimeoutPolling(Exception):
    pass

class BaseLongPollingView(View):
    timeout = 30

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        self.request = request
        self.args = args
        self.kwargs = kwargs
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
        timeout = gevent.Timeout(10, TimeoutPolling)
        timeout.start()
        try:
            for chunk in handler(self.request):
                yield chunk
        except TimeoutPolling:
            pass
        finally:
            timeout.cancel()

    def iterator(self):
        raise NotImplementedError()

