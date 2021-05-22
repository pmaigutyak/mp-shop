
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from clothes import views


app_name = 'clothes'


urlpatterns = [

    path('sizes', views.get_sizes, name='sizes')

]


app_urls = i18n_patterns(
    path('clothes/', include((urlpatterns, app_name)))
)
