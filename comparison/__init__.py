
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ComparisonAppConfig(AppConfig):

    name = 'comparison'
    verbose_name = _('Comparison')


default_app_config = 'comparison.ComparisonAppConfig'
