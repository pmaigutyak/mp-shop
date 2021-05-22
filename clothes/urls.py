
from django.urls import path, include

from clothes import views


app_name = 'clothes'


urlpatterns = [

    path('get-sizes/', views.get_sizes, name='get-sizes')

]


app_urls = [
    path('clothes/', include((urlpatterns, app_name)))
]
