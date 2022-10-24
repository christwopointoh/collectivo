"""URL patterns of the collectivo authentication module."""
from django.urls import path
from collectivo.auth import views
from django.conf import settings


app_name = 'collectivo.auth'

urlpatterns = []

if settings.DEVELOPMENT:

    urlpatterns += [
        path('api/auth-dev/v1/token/',
             views.KeycloakTokenView.as_view(),
             name='token'),
        path(
            'api/auth-dev/v1/is_authenticated/',
            views.IsAuthenticated.as_view(),
            name='is_authenticated'),
    ]
