"""
URL configuration for biorhythm_api project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('biorhythms.urls')),
]