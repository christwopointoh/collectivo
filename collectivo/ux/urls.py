"""URL patterns of the test_extension."""
from django.urls import path, include
from . import views
from collectivo.urls import urlpatterns as collectivo_urlpatterns

app_name = 'collectivo.ux'
api_path = f'api/{app_name}/'

urlpatterns = [
    path(api_path+'v1/menus/<str:menu_name>',
         views.MenuItemsReadView.as_view(), name='menu'),
]

# Include URL namespace in parent module
collectivo_urlpatterns += [
    path('', include('collectivo.ux.urls')),
]
