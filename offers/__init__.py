
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class OffersAppConfig(AppConfig):

    name = 'offers'
    verbose_name = _('Offers')


default_app_config = 'offers.OffersAppConfig'
