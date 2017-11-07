
from django.conf.urls import url, include

from shop.flags import views


urlpatterns = [

    url(r'^api/', include('shop.flags.api.urls', namespace='api')),

    url(r'^flag/(?P<flag_pk>\d+)/$', views.get_products_by_flag,
        name='products')

]
