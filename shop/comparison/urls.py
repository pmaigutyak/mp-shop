
from django.conf.urls import url

from shop.comparison import views


urlpatterns = [

    url(r'^$', views.index, name='index'),

    url(r'^add/$', views.add, name='add'),

    url(r'^remove/$', views.remove, name='remove'),

]
