from django.urls import path
from . import views

urlpatterns = [
    path('users/login/', views.login, name='login'),  # ← 放在前面
    path('users/', views.user_list, name='user_list'),
    path('users/<uuid:user_id>/', views.user_detail, name='user_detail'),
]
