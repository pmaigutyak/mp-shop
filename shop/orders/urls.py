
from django.conf.urls import url

from shop.orders import views


urlpatterns = [

    url(r'^checkout/$', views.checkout, name='checkout'),

]
