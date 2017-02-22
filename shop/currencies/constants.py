
from django.utils.translation import ugettext_lazy as _


CURRENCY_UAH = 1
CURRENCY_USD = 2
CURRENCY_EUR = 3


DEFAULT_CURRENCIES = (
    (CURRENCY_UAH, _('UAH')),
    (CURRENCY_USD, _('USD')),
    (CURRENCY_EUR, _('EUR')),
)
