"""URL patterns of the collectivo core."""
from django.urls import path, include
from collectivo import views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)

app_name = 'collectivo'


urlpatterns = [
    path('api/collectivo/v1/version/',
         views.VersionView.as_view(), name='version'),
    path('api/auth/', include('collectivo.auth.urls')),

    # API Documentation
    path('api/collectivo/v1/schema/',
         SpectacularAPIView.as_view(),
         name='api-schema'),
    path('api/docs/',
         SpectacularSwaggerView.as_view(url_name='collectivo:api-schema'),
         name='api-docs'),
]
