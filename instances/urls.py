from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path(r'<int:compute_id>/<filename:vname>/', views.instance, name='instance'),
    path(r'statistics/<int:compute_id>/<filename:vname>/', views.inst_graph, name='inst_graph'),
    path(r'status/<int:compute_id>/<filename:vname>/', views.inst_status, name='inst_status'),
    path(r'guess_mac_address/<filename:vname>/', views.guess_mac_address, name='guess_mac_address'),
    path(r'guess_clone_name/', views.guess_clone_name, name='guess_clone_name'),
    path(r'check_instance/<filename:vname>/', views.check_instance, name='check_instance'),
    path(r'sshkeys/<filename:vname>/', views.sshkeys, name='sshkeys'),
]
