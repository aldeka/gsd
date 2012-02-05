#!/usr/bin/env python
import os
import sys
import os.path

os.chdir(os.path.dirname(os.path.abspath(__file__)))	
if os.path.exists("env/bin/activate_this.py"):
    execfile("env/bin/activate_this.py", globals(), locals())

print >> sys.stderr os.path.abspath(__file__)
print >> os.getcwd()
sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
