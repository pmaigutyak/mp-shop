
from exchange.settings import ExchangeSettings
from categories.settings import CategorySettings
from attributes.settings import AttributeSettings


class CargoSettings(ExchangeSettings, CategorySettings, AttributeSettings):

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + [
            'cargo',
            'manufacturers',
            'availability'
        ]


default = CargoSettings
