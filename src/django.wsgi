import os
import sys

for path in ('/app/pygotham/django',
    '/app/pygotham/src',
    '/app/pygotham/src/utils',
    '/app/pygotham'):
    if path not in sys.path:
        sys.path.insert(0,path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'src.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

