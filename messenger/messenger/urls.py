from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),  # Админка Django
    path('login/', include('myapp.urls')),  # Подключаем URL-адреса приложения myapp
    path('register/', include('myapp.urls')),  # Подключаем URL-адреса приложения myapp
    path('success/', include('myapp.urls')),  # Подключаем URL-адреса приложения myapp
    path('', include('myapp.urls')),  # Маршрут для главной страницы
]

