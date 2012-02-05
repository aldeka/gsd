#!/usr/bin/env python
import os
import sys

sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
