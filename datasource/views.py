from django.shortcuts import render
from django.http import HttpResponse, Http404
from accounts.models import UserInstance, UserSSHKey
import json
import socket

OS_VERSIONS = [ 'latest', '' ]
OS_UUID = "iid-dswebvirtcloud"

def os_index(request):
    response = '\n'.join(OS_VERSIONS)
    return HttpResponse(response)

def os_metadata_json(request, version):
    """
    :param request:
    :param version:
    :return:
    """

    if version == 'latest':
        ip = get_client_ip(request)
        hostname = get_hostname_by_ip(ip)
        response = { 'uuid': OS_UUID, 'hostname': hostname }
        return HttpResponse(json.dumps(response))
    else:
        err = 'Invalid version: %s' % version
        raise Http404(err)

def os_userdata(request, version):
    """
    :param request:
    :param version:
    :return:
    """
    if version == 'latest':
        ip = get_client_ip(request)
        hostname = get_hostname_by_ip(ip)
        vname = hostname.split('.')[0]
        
        instance_keys = []
        userinstances = UserInstance.objects.filter(instance__name=vname)
        
        for ui in userinstances:
            keys = UserSSHKey.objects.filter(user=ui.user)
            for k in keys:
                instance_keys.append(k.keypublic)

        return render(request, 'user_data', locals())
    else:
        err = 'Invalid version: %s' % version
        raise Http404(err)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_hostname_by_ip(ip):
    addrs = socket.gethostbyaddr(ip)
    return addrs[0]
