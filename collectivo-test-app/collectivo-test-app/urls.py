"""URL Configuration of collectivo-test-app."""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('collectivo.urls')),
    path('', include('test_extension.urls'))
]

handler400 = 'rest_framework.exceptions.bad_request'
handler500 = 'rest_framework.exceptions.server_error'
