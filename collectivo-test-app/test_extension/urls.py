"""URL patterns of the test_extension extension."""
from django.urls import path
from test_extension import views

app_name = 'test_extension'


urlpatterns = [
    path('test/', views.TestView.as_view(), name='test_view'),
    path('ux/', views.fetch_ux, name='ux'),
]
