from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
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
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    url(r'^profile/$', views.profile, name='profile'), url(r'^$', views.accounts, name='accounts'),
    url(r'^profile/(?P<user_id>[0-9]+)/$', views.account, name='account'),
]
