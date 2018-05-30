"""
WSGI config for webvirtcloud project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webvirtcloud.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()



# noVNC server
import multiprocessing

def worker():
    cmd = 'python noVNC/utils/websockify --target-config=vnc_tokens 6080 >/dev/null 2>&1'
    os.system(cmd)

def start_websockify():
    t = multiprocessing.Process(target=worker)
    t.start()

start_websockify()

