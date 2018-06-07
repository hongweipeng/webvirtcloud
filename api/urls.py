from django.urls import path
from . import views

urlpatterns = [
    path('quick_vm_list/', views.QuickVMList.as_view()),
    
]