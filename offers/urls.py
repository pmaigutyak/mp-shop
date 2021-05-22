
from django.urls import path, include

from offers import views


app_name = 'offers'


urlpatterns = [

    path('modal/<int:product_id>/', views.get_price_offer_modal, name='modal'),

    path('send/<int:product_id>/', views.send_price_offer, name='send'),

]


app_urls = [
    path('offers/', include((urlpatterns, app_name)))
]

