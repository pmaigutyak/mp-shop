
from django.conf.urls import url

from shop.flags.api import views


urlpatterns = [

    url(r'^flags/$', views.get_flags, name='flags'),

]
