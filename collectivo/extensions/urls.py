"""URL patterns of extension module."""
from django.urls import path
from . import views

app_name = 'collectivo.extensions'


urlpatterns = [
    path('v1/extensions/', views.ExtensionView.as_view(),
         name='extensions'),
]
