from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.showlogs, name='showlogs'),
    path(r'<int:page>/', views.showlogs, name='showlogspage'),
    path(r'vm_logs/<filename:vname>/', views.vm_logs, name='vm_logs'),
]
