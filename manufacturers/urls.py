
from django.urls import path

from manufacturers import views


app_name = 'manufacturers'


urlpatterns = [

    path('autocomplete/', views.manufacturer_autocomplete,
         name='autocomplete')

]
