from rest_framework import generics, permissions, exceptions
from rest_framework.views import APIView, Response
from create import models as create_models
from vrtManager import taskflow_base
from vrtManager import consts
from create import taskflow_quick_vm





class QuickVMList(APIView):
    queryset = create_models.QuickVM.objects.all()
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request):
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
        
        
        if create_models.QuickVM.objects.filter(token=token).exists():
            qvm_model = create_models.QuickVM.objects.get(token=token)
            if qvm_model.status != consts.TASK_FINISH:
                raise exceptions.APIException('the model is not prepare')
        else:
            qvm_model = create_models.QuickVM(credit=credit, token=token)
            qvm_model.save()
        qvm_model.step = ""
        qvm_model.template_id = template_id
        qvm_model.save()
            
        
        eng = taskflow_base.build(qvm_model, taskflow_quick_vm.STEPS, create_models.QuickVMStep, 'quick_id')
        taskflow_base.async_run(eng, qvm_model, create_models.QuickVMStep, 'quick_id')
        
        return Response({
            'success': True
        })
        
        
        


