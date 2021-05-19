
from django.urls import path, include

from django.conf.urls.i18n import i18n_patterns

from orders import views


app_name = 'orders'


urlpatterns = [
    path('checkout/', views.checkout, name='checkout')
]


app_urls = i18n_patterns(

    path('orders/', include((urlpatterns, app_name))),

    path('delivery/', include('delivery.urls'))

)
