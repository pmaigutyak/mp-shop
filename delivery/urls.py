
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from delivery import views


app_name = 'delivery'


urlpatterns = [

    path('cities', views.get_cities, name='cities'),

    path('warehouses', views.get_warehouses, name='warehouses'),

]

app_urls = i18n_patterns(
    path('delivery', include((urlpatterns, app_name)))
)
