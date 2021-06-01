
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ClothesAppConfig(AppConfig):

    name = 'clothes'
    verbose_name = _('Clothes')


default_app_config = 'clothes.ClothesAppConfig'
