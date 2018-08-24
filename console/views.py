import re
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from instances.models import Instance
from vrtManager.instance import wvmInstance
from webvirtcloud.settings import WS_PORT
from webvirtcloud.settings import WS_PUBLIC_HOST
from webvirtcloud.settings import VNC_TOKENS_FILE
from libvirt import libvirtError
from vrtManager import tools

@login_required
def console(request):
    """
    :param request:
    :return:
    """
    token = ''
    console_error = None
    if request.method == 'GET':
        token = request.GET.get('token', '')
        view_type = request.GET.get('view', 'lite')

    try:
        temptoken = token.split('-', 1)
        host = int(temptoken[0])
        uuid = temptoken[1]
        instance = Instance.objects.get(compute_id=host, uuid=uuid)
        conn = wvmInstance(instance.compute.hostname,
                           instance.compute.login,
                           instance.compute.password,
                           instance.compute.type,
                           instance.name)
        console_type = conn.get_console_type()
        #console_websocket_port = conn.get_console_websocket_port()
        console_websocket_port = conn.get_console_port()

        console_passwd = conn.get_console_passwd()
    except libvirtError as lib_err:
        console_type = None
        console_websocket_port = None
        console_passwd = None


    # ws_port = console_websocket_port if console_websocket_port else WS_PORT
    ws_port = WS_PORT
    ws_host = WS_PUBLIC_HOST if WS_PUBLIC_HOST else request.get_host()


    vnc_host = instance.compute.hostname
    vnc_port = console_websocket_port
    #
    if ':' in ws_host:
        ws_host = re.sub(':[0-9]+', '', ws_host)
    vnc_token_lines = []
    if console_type == 'vnc':
        # 设置vnc文件
        tools.set_proxy(token, vnc_host, vnc_port)
        if console_passwd is None:
            console_passwd = ""

        #response = render(request, 'console-vnc.html', locals())
        vnc_url = reverse('vnc_auto')
        vnc_url += "?path=websockify/?token=%s&verify=%s" % (token, console_passwd)
        #_vnc_url = "http://%s:%s/vnc_auto.html?path=websockify/?token=%s&verify=%s" % (ws_host, ws_port, token, console_passwd)
        #print(_vnc_url)
        return redirect(vnc_url)

    elif console_type == 'spice':
        response = render(request, 'console-spice.html', locals())

    console_page = "console-" + console_type + "-" + view_type + ".html"
    if console_type == 'vnc' or console_type == 'spice':
        response = render(request, console_page, locals())
    else:
        console_error = "Console type: %s no support" % console_type
        response = render(request, 'console-vnc-lite.html', locals())

    response.set_cookie('token', token)
    return response


@login_required
def vnc_auto(request):
    return render(request, 'vnc_auto.html')

def vnc_allow_cors(request):
    response = render(request, 'vnc_auto.html')
    response['X-Frame-Options'] = 'ALLOW-FROM'
    response['Content-Security-Policy'] = 'frame-ancestors *'
    return response

def view_only_vnc_allow_cors(request):
    response = render(request, 'view_only_vnc_auto.html')
    response['X-Frame-Options'] = 'ALLOW-FROM'
    response['Content-Security-Policy'] = 'frame-ancestors *'
    return response
