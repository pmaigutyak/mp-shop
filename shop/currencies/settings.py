
from django.conf import settings

from shop.currencies.constants import CURRENCY_UAH, DEFAULT_CURRENCIES


CURRENCIES = getattr(settings, 'CURRENCIES', DEFAULT_CURRENCIES)

DEFAULT_CURRENCY = getattr(settings, 'DEFAULT_CURRENCY', CURRENCY_UAH)

CURRENCY_SESSION_KEY = getattr(settings, 'CURRENCIES', 'CURRENCY')
