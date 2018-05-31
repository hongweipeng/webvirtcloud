from django.conf.urls import include, url
from django.urls import path, re_path, register_converter
from django.contrib import admin
import instances.views
import storages.views
import networks.views
import computes.views
import create.views
import interfaces.views
import secrets.views
import console.views
from . import converters

register_converter(converters.FilenameConverter, 'filename')

urlpatterns =[
    path('', instances.views.index, name='index'),
    path(r'instances/', instances.views.instances, name='instances'),

    path(r'instance/', include('instances.urls')),
    path(r'accounts/', include('accounts.urls')),
    path(r'computes/', include('computes.urls')),
    path(r'logs/', include('logs.urls')),

    path(r'compute/<int:compute_id>/storages/',
        storages.views.storages, name='storages'),
    path(r'compute/<int:compute_id>/storage/<filename:pool>/',
        storages.views.storage, name='storage'),
    path(r'compute/P<int:compute_id>/networks/',
        networks.views.networks, name='networks'),
    path(r'compute/<int:compute_id>/network/<filename:pool>/',
        networks.views.network, name='network'),
    path(r'compute/P<int:compute_id>/interfaces/',
        interfaces.views.interfaces, name='interfaces'),
    path(r'compute/<int:compute_id>/interface/<filename:iface>/',
        interfaces.views.interface, name='interface'),
    path(r'compute/<int:compute_id>/secrets/',
        secrets.views.secrets, name='secrets'),
    path(r'compute/<int:compute_id>/create/',
        create.views.create_instance, name='create_instance'),

    path(r'console/', console.views.console, name='console'),
    path(r'vnc_auto/', console.views.vnc_auto, name='vnc_auto'),
    path(r'admin/', admin.site.urls),
]
