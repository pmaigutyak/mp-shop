
from django.conf.urls import url

from delivery import views


app_name = 'delivery'


urlpatterns = [

    url('cities', views.get_cities, name='cities'),

    url('warehouses', views.get_warehouses, name='warehouses'),

]
