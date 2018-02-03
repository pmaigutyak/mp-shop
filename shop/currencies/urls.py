
from django.conf.urls import url

from shop.currencies import views


app_name = 'currencies'


urlpatterns = [

    url(r'^set-currency/$', views.set_currency, name='set-currency')

]
