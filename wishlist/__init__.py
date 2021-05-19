
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class WishListAppConfig(AppConfig):

    name = 'wishlist'
    verbose_name = _('WishList')


default_app_config = 'wishlist.WishListAppConfig'
