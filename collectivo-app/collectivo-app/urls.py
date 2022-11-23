"""URL Configuration of collectivo-app."""
from django.urls import path, include


urlpatterns = [path('', include('collectivo.urls'))]

# Try to import custom urls
try:
    from extensions import urls
    urlpatterns += urls.urlpatterns
except ModuleNotFoundError:
    pass

handler400 = 'rest_framework.exceptions.bad_request'
handler500 = 'rest_framework.exceptions.server_error'
