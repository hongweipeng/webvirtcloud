from django.conf.urls import url
from django.urls import path
from . import views
import django.contrib.auth.views

urlpatterns = [
    path(r'', views.accounts, name='accounts'),
    path(r'login/', django.contrib.auth.views.login,
        {'template_name': 'login.html'}, name='login'),
    path(r'logout/', django.contrib.auth.views.logout,
        {'template_name': 'logout.html'}, name='logout'),
    path(r'profile/', views.profile, name='profile'),
    path(r'profile/<filename:user_id>/', views.account, name='account'),
]
