"""URL Configuration of collectivo_app."""
import logging

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

logger = logging.getLogger(__name__)

urlpatterns = [
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Extensions
for app in settings.COLLECTIVO["extensions"]:
    try:
        pattern = path("", include(f"{app}.urls"))
        urlpatterns.append(pattern)
    except ModuleNotFoundError:
        pass  # If there is no urls.py, continue without error
    except Exception as e:
        logger.error(f"Error reading urls.py for {app}: {e}", exc_info=True)

# API Documentation
if settings.COLLECTIVO["api_docs"]:
    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
        path(
            "api/docs/",
            SpectacularSwaggerView.as_view(url_name="api-schema"),
            name="api-docs",
        ),
    ]

handler400 = "rest_framework.exceptions.bad_request"
handler500 = "rest_framework.exceptions.server_error"
