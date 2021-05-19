
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DeliveryAppConfig(AppConfig):
    name = 'delivery'
    verbose_name = _('Delivery')


default_app_config = 'delivery.DeliveryAppConfig'
