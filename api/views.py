import time
from django.urls import reverse
from rest_framework import generics, permissions, exceptions
from rest_framework.views import APIView, Response
from rest_framework.decorators import api_view
from create import models as create_models
from vrtManager import taskflow_base
from vrtManager import consts
from create import taskflow_quick_vm
from vrtManager.instance import wvmInstance

from vrtManager import tools
from webvirtcloud.settings import WS_PORT
from webvirtcloud.settings import WS_PUBLIC_HOST
from webvirtcloud.settings import VNC_TOKENS_FILE
from rest_framework.request import Request
from django.contrib.auth import authenticate
from accounts.models import UserInstance
from vrtManager import tools

def api_auth_check(request: Request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    if not user:
        raise exceptions.ValidationError('username or password error')

    timestamp = data.get('timestamp')
    checkcode = data.get('checkcode')
    if not timestamp or not checkcode:
        raise exceptions.ValidationError('checkcode error')


    code = tools.md5(password + chr(163) + str(timestamp) + 'jxkj')
    if checkcode != code:
        raise exceptions.ValidationError('checkcode error')

    return user

class QuickVMList(APIView):
    queryset = create_models.QuickVM.objects.all()
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request):
        user = api_auth_check(request)
        data = request.data
        print(data)
        # 验证必填的参数
        credit = data.get('credit')
        if not credit:
            raise exceptions.ValidationError('key "credit" is null or empty')
        
        token = data.get('token')
        if not token:
            raise exceptions.ValidationError('key "token" is null or empty')
        
        template_id = int(data.get('template_id'))
        if not template_id or not create_models.VMTemplate.objects.filter(pk=template_id).exists():
            raise exceptions.ValidationError('key "template_id" is null or empty or template not exists')

        is_async = data.get('async', False)
        reuse_computer = data.get('reuse_computer', True)
        
        if create_models.QuickVM.objects.filter(token=token).exists():
            qvm_model = create_models.QuickVM.objects.get(token=token)
            if qvm_model.status != consts.TASK_FINISH and not reuse_computer:
                raise exceptions.APIException('the model is not prepare')
        else:
            qvm_model = create_models.QuickVM(credit=credit, token=token)
            qvm_model.save()
        qvm_model.step = ""
        qvm_model.template_id = template_id
        qvm_model.save()
            
        
        eng = taskflow_base.build(qvm_model, taskflow_quick_vm.STEPS, create_models.QuickVMStep, 'quick_id')
        if is_async:
            taskflow_base.async_run(eng, qvm_model, create_models.QuickVMStep, 'quick_id')
            return Response({
                'success': True
            })

        # 同步
        taskflow_base.sync_run(eng, qvm_model, create_models.QuickVMStep, 'quick_id')


        # 返回 vnc 地址
        instance = qvm_model.instance

        if not instance:
            return Response({
                'success': False,
                'msg': 'can not find idle compute'
            })

        uuid = instance.uuid
        conn = wvmInstance(instance.compute.hostname,
                           instance.compute.login,
                           instance.compute.password,
                           instance.compute.type,
                           instance.name)
        console_type = conn.get_console_type()
        console_websocket_port = conn.get_console_port()
        console_passwd = conn.get_console_passwd()

        token = '%d-%s' % (instance.id, uuid)
        vnc_host = instance.compute.hostname
        vnc_port = console_websocket_port
        tools.set_proxy(token, vnc_host, vnc_port)

        if console_passwd is None:
            console_passwd = ""

        vnc_url = reverse('vnc_allow_cors')
        vnc_url += "?path=websockify/?token=%s&verify=%s" % (token, console_passwd)

        view_only_vnc_url = reverse('view_only_vnc_allow_cors')
        view_only_vnc_url += "?path=websockify/?token=%s&verify=%s" % (token, console_passwd)

        return Response({
            'success': True,
            'instance_id': instance.id,
            'vnc_url': '%s://%s' % (request.scheme, request._get_raw_host() + vnc_url),
            'view_only_vnc_url': '%s://%s' % (request.scheme, request._get_raw_host() + view_only_vnc_url),
        })




class ScreenShot(APIView):
    queryset = UserInstance.objects.all()
    permission_classes = (permissions.AllowAny, )  # 使用自定义的认证方式，因此rest ful不对此进行验证
    def post(self, request, instance_id):
        if request.method != 'POST':
            raise exceptions.ValidationError('method not allow')
        user = api_auth_check(request)
        userinstace = None
        try:
            userinstace = UserInstance.objects.get(instance__id=instance_id,
                                                   user__id=user.id)
        except UserInstance.DoesNotExist:
            raise exceptions.ValidationError('the vm id %s is not exist' % instance_id)
        compute = userinstace.instance.compute
        conn = wvmInstance(compute.hostname,
                           compute.login,
                           compute.password,
                           compute.type,
                           userinstace.instance.name)

        img_base64 = conn.get_screenshot()
        conn.close()
        return Response({
            'success': True,
            'data': img_base64,
        })


class ShutDownVm(APIView):
    qeryset = ()
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        user = api_auth_check(request)
        instance_id = request.data.get('instance_id')
        try:
            userinstace = create_models.QuickVM.objects.get(instance__id=instance_id)
        except create_models.QuickVM.DoesNotExist:
            raise exceptions.ValidationError('the vm id %s is not exist' % instance_id)

        compute = userinstace.instance.compute
        conn = wvmInstance(compute.hostname,
                           compute.login,
                           compute.password,
                           compute.type,
                           userinstace.instance.name)

        conn.shutdown()
        conn.close()
        return Response({
            'success': True,
        })


