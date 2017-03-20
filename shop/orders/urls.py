
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from shop.orders import views


urlpatterns = [

    url(r'^checkout/$', views.checkout, name='checkout'),

    url(r'^order-history/$', views.order_history, name='history'),

    url(r'^invoice/(?P<pk>\d+)/download/$',
        login_required(views.OrderInvoiceDownloadView.as_view()),
        name='download-invoice'),

]
