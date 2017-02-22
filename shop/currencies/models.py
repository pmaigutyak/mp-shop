
from django.db import models
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _

from shop.lib import format_number
from shop.currencies.lib import format_printable_price
from shop.currencies.constants import CURRENCY_UAH, CURRENCY_EUR, CURRENCY_USD
from shop.currencies.settings import CURRENCIES


class ExchangeRate(models.Model):

    currency = models.PositiveIntegerField(
        _('Currency'), choices=CURRENCIES, unique=True)

    value = models.FloatField(_('Value'), default=0)

    def __unicode__(self):
        return '%s: %s' % (self.get_currency_display(), self.value)

    @classmethod
    def get_exchange_rates(cls):

        exchange_rates = cache.get('exchange_rates', {})

        if not exchange_rates:

            exchange_rates = {c: 1 for c, n in CURRENCIES}

            for exchange_rate in cls.objects.all():
                exchange_rates[exchange_rate.currency] = exchange_rate.value

            cache.set('exchange_rates', exchange_rates, 240)

        return exchange_rates

    @classmethod
    def convert(cls, price, src_currency, dst_currency,
                format_price=False, printable=False):

        exchange_rates = cls.get_exchange_rates()

        if src_currency is dst_currency:
            new_price = price

        elif src_currency is CURRENCY_UAH and dst_currency is CURRENCY_USD:
            new_price = price / exchange_rates[CURRENCY_USD]

        elif src_currency is CURRENCY_UAH and dst_currency is CURRENCY_EUR:
            new_price = price / exchange_rates[CURRENCY_EUR]

        elif src_currency is CURRENCY_USD and dst_currency is CURRENCY_UAH:
            new_price = price * exchange_rates[CURRENCY_USD]

        elif src_currency is CURRENCY_EUR and dst_currency is CURRENCY_UAH:
            new_price = price * exchange_rates[CURRENCY_EUR]

        elif src_currency is CURRENCY_USD and dst_currency is CURRENCY_EUR:
            new_price = (price / exchange_rates[CURRENCY_EUR]) * \
                   exchange_rates[CURRENCY_USD]

        elif src_currency is CURRENCY_EUR and dst_currency is CURRENCY_USD:
            new_price = (price / exchange_rates[CURRENCY_USD]) * \
                   exchange_rates[CURRENCY_EUR]
        else:
            raise ValueError(
                'Unknown currency %s/%s' % (dst_currency, src_currency))

        if format_price and not printable:
            new_price = format_number(new_price)

        if printable:
            new_price = format_printable_price(new_price, dst_currency)

        return new_price

    class Meta:
        verbose_name = _('Exchange rate')
        verbose_name_plural = _('Exchange rate')
