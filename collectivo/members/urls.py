"""URL patterns of the members extension."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from collectivo.routers import DirectDetailRouter
from . import views


app_name = 'collectivo.members'

admin_router = DefaultRouter()
admin_router.register(
    'members', views.MembersAdminViewSet, basename='member')
admin_router.register(
    'summary', views.MembersAdminSummaryView, basename='summary')

me_router = DirectDetailRouter()
me_router.register(
    'register', views.MemberRegisterView, basename='register')
me_router.register(
    'profile', views.MemberViewSet, basename='profile')

urlpatterns = [
    path('api/members/v1/', include(admin_router.urls)),
    path('api/members/v1/', include(me_router.urls)),
]
