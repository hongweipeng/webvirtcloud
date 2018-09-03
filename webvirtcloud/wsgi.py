"""
WSGI config for webvirtcloud project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
import sys
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webvirtcloud.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()



# noVNC server
import subprocess
from vrtManager import websockify
from webvirtcloud.settings import WS_PORT
from webvirtcloud.settings import WS_PUBLIC_HOST
from webvirtcloud.settings import VNC_TOKENS_FILE
import threading
import multiprocessing
import websockify
from websockify.token_plugins import TokenFile
class MyProxyRequestHandler(websockify.ProxyRequestHandler):
	buffer_size = 65536 * 216

def worker():
    # server = websockify.WebSocketProxy(listen_port=WS_PORT, target_cfg=VNC_TOKENS_FILE,)
    # server.start_server()
    args = [sys.executable, 'noVNC/utils/websockify', '--target-config=%s' % VNC_TOKENS_FILE,  str(WS_PORT), '>/dev/null 2>&1', ]
    new_environ = os.environ.copy()
    new_environ["RUN_MAIN"] = 'true'
    print(' '.join(args))
    exit_code = subprocess.call(args, env=new_environ)
    print('websockify exit_code:', exit_code)
    # if exit_code != 3:
    #     return exit_code


    # cmd = 'python noVNC/utils/websockify --target-config=vnc_tokens 6080 >/dev/null 2>&1'
    # subprocess.Popen(cmd)
    # os.system(cmd)

def start_websockify():
    #t = threading.Thread(target=worker)
    #t.start()
    websockify.logger_init()
    data = {
        #'target_cfg': VNC_TOKENS_FILE,
        'listen_port': 6080,
    }
    target_cfg = VNC_TOKENS_FILE
    target_cfg = os.path.abspath(target_cfg)
    token_plugin = TokenFile(target_cfg)
    data['token_plugin'] = token_plugin

    ws_proxy = websockify.WebSocketProxy(**data, RequestHandlerClass=MyProxyRequestHandler)
    ws_proxy.start_server()

multiprocessing.Process(target=start_websockify,).start()
#threading.Thread(target=start_websockify, daemon=True).start()

# 计划任务 server
from crontab import scheduler
scheduler.start()


