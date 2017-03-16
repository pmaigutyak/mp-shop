
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from shop.orders.constants import *


DEFAULT_DELIVERY_METHODS = (
    (DELIVERY_METHOD_SELF, _('Self delivery')),
    (DELIVERY_METHOD_NOVA_POSHTA, _('Nova Poshta')),
    (DELIVERY_METHOD_INTIME, _('In Time')),
    (DELIVERY_METHOD_GUNSEL, _('Gunsel')),
    (DELIVERY_METHOD_AVTOLUKS, _('Avtoluks')),
    (DELIVERY_METHOD_OTHER, _('Other')),
)

DEFAULT_PAYMENT_METHODS = (
    (PAYMENT_METHOD_CASH, _('Cash payment')),
    (PAYMENT_METHOD_CASHLESS, _('Cashless payment')),
    (PAYMENT_METHOD_COD, _('C.O.D.')),
    (PAYMENT_METHOD_PRIVAT24, _('Privat24 Payment')),
)

DEFAULT_STATUSES = (
    (STATUS_NOT_REVIEWED, _('Not reviewed')),
    (STATUS_PROCESSING, _('Processing')),
    (STATUS_CANCELED, _('Canceled')),
    (STATUS_COMPLETED, _('Completed')),
)

ORDER_PAYMENT_METHODS = getattr(
    settings, 'ORDER_PAYMENT_METHODS', DEFAULT_PAYMENT_METHODS)

ORDER_DELIVERY_METHODS = getattr(
    settings, 'ORDER_DELIVERY_METHODS', DEFAULT_DELIVERY_METHODS)

ORDER_STATUSES = getattr(settings, 'ORDER_STATUSES', DEFAULT_STATUSES)

ORDER_INVOICE_MOBILE = getattr(settings, 'ORDER_INVOICE_MOBILE', '')

ORDER_INVOICE_EMAIL = getattr(settings, 'ORDER_INVOICE_EMAIL', '')

DEFAULT_DELIVERY_METHOD = getattr(settings, 'DEFAULT_DELIVERY_METHOD', None)

DEFAULT_PAYMENT_METHOD = getattr(settings, 'DEFAULT_PAYMENT_METHOD', None)

DEFAULT_STATUS = getattr(settings, 'DEFAULT_STATUS', STATUS_NOT_REVIEWED)

POST_OFFICE_CHOICES = getattr(settings, 'POST_OFFICE_CHOICES', None)
