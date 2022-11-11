"""URL Configuration of collectivo-test-app."""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('collectivo.urls')),
    path('', include('test_extension.urls'))
]
