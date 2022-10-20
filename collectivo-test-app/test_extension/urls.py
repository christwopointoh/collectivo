"""URL patterns of the test_extension."""
from django.urls import path
from test_extension import views


app_name = 'test_extension'
api_path = f'api/{app_name}/'

urlpatterns = [
    path(api_path+'v1/test/', views.TestAPIView.as_view(), name='test_api'),
    path(app_name+'/', views.test_html_view, name='test_html'),
]
