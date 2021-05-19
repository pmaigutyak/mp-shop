
from django.utils.translation import ugettext_lazy as _


CURRENCY_UAH = 980
CURRENCY_USD = 840
CURRENCY_EUR = 978

CURRENCIES = (
    (CURRENCY_UAH, _('UAH')),
    (CURRENCY_USD, _('USD')),
    (CURRENCY_EUR, _('EUR')),
)

CURRENCY_NAMES = {
    CURRENCY_UAH: 'uah',
    CURRENCY_USD: 'usd',
    CURRENCY_EUR: 'eur'
}

DEFAULT_CURRENCY = CURRENCY_UAH

CURRENCY_SESSION_KEY = 'CURRENCY'
