from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('login/', views.user_login, name='login'),  # Страница входа
    path('register/', views.register, name='register'),  # Страница регистрации
    path('success/', views.success, name='success'),  # Страница успеха
    path('chat/', views.chat, name='chat'),  # Страница чата
    path('chat/<int:dialog_id>/', views.chat, name='chat'),  # Страница чата с диалогом
    path('logout/', views.user_logout, name='logout'),  # Выход из системы
]