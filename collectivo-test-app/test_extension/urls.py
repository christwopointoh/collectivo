"""URL patterns of the test_extension extension."""
from django.urls import path
from test_extension import views

app_name = 'test_extension'
api_path = f'api/{app_name}/'

urlpatterns = [
    path(api_path+'v1/test/', views.TestView.as_view(), name='test_view'),
]
