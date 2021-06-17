
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from labels import views


app_name = 'labels'


urlpatterns = [

    path('', views.get_labels, name='list'),

    path('products/<label_id>/', views.get_products_by_label, name='products')

]

app_urls = i18n_patterns(

    path('labels/', include((urlpatterns, app_name)))

)
