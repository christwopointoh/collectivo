"""URL patterns of the test_extension."""
from django.urls import path
from test_extension import views
from collectivo.urls import urlpatterns as collectivo_urlpatterns

app_name = 'test_extension'
api_path = f'api/{app_name}/'

urlpatterns = [
    path(api_path+'v1/test/', views.TestView.as_view(), name='test_view'),
]

collectivo_urlpatterns += urlpatterns
