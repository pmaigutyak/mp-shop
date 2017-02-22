
from shop.lib import format_price
from shop.currencies.settings import CURRENCIES, DEFAULT_CURRENCY


def format_printable_price(price, currency=DEFAULT_CURRENCY):
    return '%s %s' % (format_price(price), dict(CURRENCIES)[currency])
