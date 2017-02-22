
from django.conf.urls import url

from shop.currencies import views


urlpatterns = [

    url(r'^set-currency/$', views.SetCurrencyView.as_view(),
        name='set-currency')

]
