"""URL patterns of the collectivo auth extension."""
from django.urls import path
from collectivo.auth import views

app_name = 'collectivo.auth'


urlpatterns = [
    path('dev/token/', views.KeycloakTokenView.as_view(), name='token'),
    path(
        'dev/is_authenticated/',
        views.IsAuthenticated.as_view(),
        name='is_authenticated'),
]
