
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CategoriesAppConfig(AppConfig):

    name = 'categories'
    verbose_name = _('Categories')


default_app_config = 'categories.CategoriesAppConfig'
