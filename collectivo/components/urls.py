"""URL patterns of the components module."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "collectivo.components"

router = DefaultRouter()
router.register("components", views.ComponentViewSet)

urlpatterns = [path("api/components/", include(router.urls))]
