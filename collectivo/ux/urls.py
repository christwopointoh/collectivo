"""URL patterns of the user experience module."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'collectivo.ux'

router = DefaultRouter()
router.register('microfrontends', views.MicroFrontendViewSet)

urlpatterns = [
    path('api/ux/v1/', include(router.urls)),
    path('api/ux/v1/menus/<str:menu_name>',
         views.MenuItemsReadView.as_view(), name='menu'),
]
