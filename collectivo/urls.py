"""URL patterns of the collectivo core."""
from django.urls import path, re_path, include
from django.conf import settings
from django.contrib.staticfiles import views as staticviews
from collectivo import views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)
from collectivo.extensions import extensions

app_name = 'collectivo'


urlpatterns = [

    # Core API views
    path('api/collectivo/v1/version/',
         views.VersionView.as_view(), name='version'),
    path('api/collectivo/', include('collectivo.extensions.urls')),

    # API Documentation
    path('api/collectivo/v1/schema/',
         SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/',
         SpectacularSwaggerView.as_view(url_name='collectivo:api-schema'),
         name='api-docs'),

]


# Add registered extensions to urlpatterns
# TODO Handle namespace conflicts
for ext in extensions.get_configs():
    urlpatterns += [
        path('', include(f'{ext.name}.urls')),
    ]


# For development
if settings.DEBUG:

    urlpatterns += [
        # Access static files
        re_path(r'^static/(?P<path>.*)$', staticviews.serve),

        # Test authentication
        path('api/collectivo-dev/', include('collectivo.auth.urls')),
    ]

