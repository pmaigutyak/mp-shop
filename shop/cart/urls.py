
from django.conf.urls import url

from shop.cart import views


urlpatterns = [

    url(r'^$', views.index, name='index'),

    url(r'^add/$', views.add, name='add'),

    url(r'^remove/$', views.remove, name='remove'),

    url(r'^set-qty/$', views.set_qty, name='set-qty'),

]
