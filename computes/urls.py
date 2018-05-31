from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.computes, name='computes'),
    path(r'overview/<int:compute_id>/', views.overview, name='overview'),
    path(r'statistics/<int:compute_id>/', views.compute_graph, name='compute_graph'),
]
