
from django.conf.urls import url

from shop.products.api import views


urlpatterns = [

    url(r'^categories/$', views.get_categories, name='categories'),

]
