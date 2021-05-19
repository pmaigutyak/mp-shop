
from django.urls import path

from wishlist import views


app_name = 'wishlist'


urlpatterns = [

    path('add/<int:product_id>/', views.add, name='add'),

    path('remove/<int:product_id>/', views.remove, name='remove')

]
