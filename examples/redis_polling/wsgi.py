import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except ImportError:
    # django 1.3
    from django.core.handlers.wsgi import WSGIHandler
    application = WSGIHandler()
