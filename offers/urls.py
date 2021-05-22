
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from offers import views


app_name = 'offers'


urlpatterns = [

    path('modal/<int:product_id>/', views.get_price_offer_modal, name='modal'),

    path('send/<int:product_id>/', views.send_price_offer, name='send'),

]


app_urls = i18n_patterns(
    path('offers/', include((urlpatterns, app_name)))
)
