"""URL patterns of the collectivo authentication module."""
from django.urls import path
from collectivo.auth import views
from django.conf import settings


app_name = 'collectivo.auth'


urlpatterns = [
    path(
        'api/keycloak/v1/test_public/',
        views.PublicTestView.as_view(),
        name='test_view_public'
    ),
    path(
        'api/keycloak/v1/test_private/',
        views.PrivateTestView.as_view(),
        name='test_view_private'
    ),
    path(
        'api/keycloak/v1/test_admin/',
        views.AdminTestView.as_view(),
        name='test_view_admin'
    ),
    path(
        'api/keycloak/v1/is_authenticated/',
        views.IsAuthenticatedView.as_view(),
        name='is_authenticated'),
]

if settings.DEVELOPMENT:

    urlpatterns += [
        path('api/keycloak/v1/token/',
             views.KeycloakTokenView.as_view(),
             name='token'),
    ]
