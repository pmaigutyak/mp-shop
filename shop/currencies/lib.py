
from shop.lib import format_price

from shop.currencies.models import ExchangeRate
from shop.currencies.settings import CURRENCIES, DEFAULT_CURRENCY


def format_printable_price(price, currency=DEFAULT_CURRENCY):
    return '%s %s' % (format_price(price), dict(CURRENCIES)[currency])


class Price(object):

    def __init__(self, obj):
        self.obj = obj

    @property
    def currency(self):
        return self.obj.currency

    def printable_currency(self):
        return self.obj.get_currency_display()

    @property
    def default(self):
        return ExchangeRate.convert(
            price=self.obj.price_in_currency,
            src_currency=self.obj.currency,
            dst_currency=DEFAULT_CURRENCY)

    @property
    def printable_default(self):
        return ExchangeRate.convert(
            price=self.obj.price_in_currency,
            src_currency=self.obj.currency,
            dst_currency=DEFAULT_CURRENCY,
            printable=True)

    @property
    def initial(self):
        return self.obj.price_in_currency

    @property
    def printable_initial(self):
        return format_printable_price(self.initial, self.currency)
