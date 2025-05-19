# backend_museo_crud/backend_museo_crud/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), # Incluye las URLs de tu aplicación 'api'
    # Si quieres versionar tu API, podrías hacer algo como:
    # path('api/v1/', include('api.urls')),
]