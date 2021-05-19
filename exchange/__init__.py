
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ExchangeAppConfig(AppConfig):

    name = 'exchange'
    verbose_name = _('Exchange')


default_app_config = 'exchange.ExchangeAppConfig'
