"""URL patterns of the user experience module."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'collectivo.ux'

router = DefaultRouter()
router.register('menus', views.MenuViewSet)
router.register(r'menus/(?P<menu_id>\w+)/items', views.MenuItemViewSet)

urlpatterns = [
    path('api/ux/v1/', include(router.urls)),
]
