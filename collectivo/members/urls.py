"""URL patterns of the members extension."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from collectivo.utils import DirectDetailRouter
from . import views


app_name = 'collectivo.members'

admin_router = DefaultRouter()
admin_router.register('members', views.MembersAdminViewSet, basename='member')

me_router = DirectDetailRouter()
me_router.register('me', views.MembersViewSet, basename='me')

urlpatterns = [
    path('api/members/v1/', include(admin_router.urls)),
    path('api/members/v1/', include(me_router.urls)),
]
