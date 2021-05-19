
from delivery.settings import DeliverySettings


class OrdersSettings(DeliverySettings):

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + [
            'orders'
        ]


default = OrdersSettings
