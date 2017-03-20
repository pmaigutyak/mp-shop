
from django.conf.urls import url

from shop.offers import views


urlpatterns = [

    url(r'^modal/(?P<product_pk>\d+)/$', views.get_price_offer_modal,
        name='modal'),

    url(r'^send/(?P<product_pk>\d+)/$', views.send_price_offer, name='send'),

]
