from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),  # Админка Django
    path('', include('myapp.urls')),  # Подключаем URL-адреса приложения myapp
]


