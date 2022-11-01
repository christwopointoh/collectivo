"""URL patterns of the members extension."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from collectivo.routers import DirectDetailRouter
from .views import MemberViewSet, MembersAdminViewSet


app_name = 'collectivo.members'

admin_router = DefaultRouter()
admin_router.register('members', MembersAdminViewSet, basename='member')

me_router = DirectDetailRouter()
me_router.register('me', MemberViewSet, basename='me')

urlpatterns = [
    path('api/members/v1/', include(admin_router.urls)),
    path('api/members/v1/', include(me_router.urls)),
]
