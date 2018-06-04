from django.urls import path
from . import views

urlpatterns = [
    
    # 宿主列表
    path('computers/', views.ComputerList.as_view()),
    #path('computers/<int:pk>/', views.ComputerList.as_view()),
]





