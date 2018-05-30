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
from vrtManager import websockify


# noVNC server
from webvirtcloud.settings import WS_PORT
from webvirtcloud.settings import WS_PUBLIC_HOST
from webvirtcloud.settings import VNC_TOKENS_FILE
import multiprocessing

def worker():
    server = websockify.WebSocketProxy(listen_port=WS_PORT, target_cfg=VNC_TOKENS_FILE,)
    server.start_server()

    #cmd = 'python noVNC/utils/websockify --target-config=vnc_tokens 6080 >/dev/null 2>&1'
    #os.system(cmd)

def start_websockify():
    t = multiprocessing.Process(target=worker)
    t.start()

start_websockify()

