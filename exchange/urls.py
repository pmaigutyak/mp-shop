
from django.urls import path, include

from exchange import views


app_name = 'exchange'


urlpatterns = [

    path('set-currency/', views.set_currency, name='set-currency')

]


app_urls = [
    path('exchange/', include((urlpatterns, app_name)))
]

