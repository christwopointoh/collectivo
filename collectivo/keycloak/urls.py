"""URL patterns of the collectivo authentication module."""
from django.urls import path
from collectivo.keycloak import views
from django.conf import settings


app_name = 'collectivo.keycloak'

urlpatterns = []

if settings.DEBUG:

    urlpatterns += [
        path('api/keycloak-dev/v1/token/',
             views.KeycloakTokenView.as_view(),
             name='token'),
        path(
            'api/keycloak-dev/v1/is_authenticated/',
            views.IsAuthenticated.as_view(),
            name='is_authenticated'),
    ]
