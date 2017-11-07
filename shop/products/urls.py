
from django.conf.urls import url, include
from django.views.generic import TemplateView

from shop.products import views


urlpatterns = [

    url(r'^api/', include('shop.products.api.urls', namespace='api')),

    url(r'^$',
        TemplateView.as_view(template_name='products/categories.html'),
        name='index'),

    url(r'^search/$', views.product_search, name='search'),

    url(r'^(?P<product_slug>[\w-]*)_(?P<product_pk>\d+)/$',
        views.ProductInfoView.as_view(), name='info'),

    url(r'^category/(?P<category_slug>[\w-]+(/[\w-]+)*)_'
        r'(?P<category_pk>\d+)/$', views.product_list, name='category'),

]
