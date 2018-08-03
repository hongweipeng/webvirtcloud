from django.urls import path
from . import views

urlpatterns = [
    path('quick_vm_list/', views.QuickVMList.as_view()),
    path('shutdown_vm/', views.ShutDownVm.as_view()),
    path('screenshot/<int:instance_id>/', views.ScreenShot.as_view()),
]