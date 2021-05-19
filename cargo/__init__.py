
from django.apps import apps, AppConfig
from django.utils.translation import ugettext_lazy as _


class CargoAppConfig(AppConfig):

    name = 'cargo'
    verbose_name = _('Cargo')

    def ready(self):

        model = apps.get_model('products', 'Product')

        from exchange.models import subscribe_on_exchange_rates
        subscribe_on_exchange_rates(model)

        from modeltranslation.translator import translator
        translator.register(model, fields=model.get_translation_fields())


default_app_config = 'cargo.CargoAppConfig'
