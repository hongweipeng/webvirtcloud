from django.urls import path
from . import views

urlpatterns = [
    
    # 宿主列表
    path('computers/', views.ComputerList.as_view(), name='rest_computers'),
    path('computers/<int:pk>/', views.ComputerDetail.as_view()),
    
    # vm模板列表
    path('vm_templates/', views.VMTempList.as_view(), name='rest_vm_templates'),
    
    
    
    
]





