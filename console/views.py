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


@login_required
def console(request):
    """
    :param request:
    :return:
    """
    token = ''
    if request.method == 'GET':
        token = request.GET.get('token', '')

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

    if console_type == 'vnc':
    #     # 设置vnc文件
        with open(VNC_TOKENS_FILE, "r+") as f:
            for line in [l.strip() for l in f.readlines()]:
                if line and not line.startswith('#'):
                    ttoken, target = line.split(': ')
                    vnc_ip, _vnc_port = target.split(':')
                    if vnc_ip == vnc_host and vnc_port == _vnc_port:
                        break       # 已配置，跳过
            else:
                vnc_info = "%s: %s:%s" % (token, vnc_host, vnc_port)
                f.writelines(["\n", vnc_info])
        if console_passwd is None:
            console_passwd = ""

        response = render(request, 'console-vnc.html', locals())

        vnc_url = "http://%s:%s/vnc_auto.html?path=websockify/?token=%s&verify=%s" % (ws_host, ws_port, token, console_passwd)
        print(vnc_url)
        return redirect(vnc_url)

    elif console_type == 'spice':
        response = render(request, 'console-spice.html', locals())
    else:
        response = "Console type %s no support" % console_type

    response.set_cookie('token', token)
    return response
