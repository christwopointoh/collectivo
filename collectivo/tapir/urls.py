"""URL patterns of the extension."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TapirViewSet


app_name = 'collectivo.tapir'

router = DefaultRouter()
# router.register('tapirmodel', TapirViewSet)


urlpatterns = [
    path('api/tapir/', include(router.urls)),
]
