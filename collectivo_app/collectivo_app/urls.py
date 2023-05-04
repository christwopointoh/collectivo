"""URL Configuration of collectivo_app."""
import logging

from django.contrib import admin
from django.urls import include, path

logger = logging.getLogger(__name__)

urlpatterns = [
    path("admin/", admin.site.urls),
]

# TODO: System to include urls of other apps

try:
    urlpatterns.append(path("", include("collectivo.urls")))
except Exception as e:
    logger.error(
        f"Error setting up collectivo url patterns: {e}", exc_info=True
    )

handler400 = "rest_framework.exceptions.bad_request"
handler500 = "rest_framework.exceptions.server_error"
