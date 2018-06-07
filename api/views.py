from rest_framework import generics, permissions
from rest_framework.views import APIView, Response
from create import models as create_models
from vrtManager import taskflow_base
from create import taskflow_quick_vm





class QuickVMList(APIView):
    queryset = create_models.QuickVM.objects.all()
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request):
        data = request.data
        qvm_model = create_models.QuickVM(credit='', token='fadfas')
        qvm_model.save()
        
        eng = taskflow_base.build(qvm_model, taskflow_quick_vm.STEPS, create_models.QuickVMStep, 'quick_id')
        taskflow_base.async_run(eng, qvm_model, create_models.QuickVMStep, 'quick_id')
        
        return Response({
            'success': True
        })
        
        
        


