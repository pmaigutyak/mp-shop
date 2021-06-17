
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class LabelsAppConfig(AppConfig):

    name = 'labels'
    verbose_name = _('Labels')


default_app_config = 'labels.LabelsAppConfig'
