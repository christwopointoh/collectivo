from django.urls import path

from core import views


app_name = 'core'

urlpatterns = [
    path('version/', views.GetVersion.as_view(), name='version'),
]
