
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from solo.models import SingletonModel

from basement.services import register_service

from exchange.utils import format_printable_price, get_price_factory
from exchange.managers import MultiCurrencyManager
from exchange.services import ExchangeService
from exchange.constants import (
    CURRENCY_UAH,
    CURRENCIES,
    CURRENCY_NAMES
)


_MULTI_CURRENCY_MODELS = set()


class ExchangeRates(SingletonModel):

    usd = models.FloatField(_('USD'), default=1)

    eur = models.FloatField(_('EUR'), default=1)

    usd_eur = models.FloatField(_('USD - EUR'), default=1)

    @classmethod
    def get(cls):
        rates, created = cls.objects.get_or_create()
        return rates

    def __str__(self):
        return ugettext('Exchange rates')

    class Meta:
        verbose_name = _('Exchange rates')
        verbose_name_plural = _('Exchange rates')


class CurrencyField(models.PositiveIntegerField):

    def __init__(
            self,
            verbose_name=_('Currency'),
            choices=CURRENCIES,
            **kwargs):
        super().__init__(
            verbose_name=verbose_name,
            choices=choices,
            **kwargs
        )


class MultiCurrencyPrice(models.Model):

    price_retail = models.FloatField(_('Retail price'))

    price_wholesale = models.FloatField(
        _('Wholesale price'),
        default=0)

    price_usd = models.FloatField(default=0)

    price_eur = models.FloatField(default=0)

    price_uah = models.FloatField(default=0)

    initial_currency = CurrencyField(default=CURRENCY_UAH)

    objects = MultiCurrencyManager()

    def save(self, **kwargs):

        rates = ExchangeRates.get()

        field = lambda c: 'price_{}'.format(CURRENCY_NAMES[c])

        for dst, dst_name in CURRENCIES:

            price_factory = get_price_factory(
                rates,
                self.initial_currency,
                dst)

            setattr(self, field(dst), price_factory(self.price_retail))

        super().save(**kwargs)

    @property
    def price(self):
        return getattr(self, 'price_{}'.format(CURRENCY_NAMES[self.currency]))

    @property
    def printable_price(self):
        return format_printable_price(self.price, self.currency)

    @property
    def currency(self):
        return getattr(self, 'annotated_currency', CURRENCY_UAH)

    @property
    def printable_price(self):
        return format_printable_price(self.price, self.currency)

    @property
    def schema_price(self):
        return str(self.price).replace(',', '.')

    @property
    def schema_currency(self):
        return CURRENCY_NAMES[self.currency].upper()

    @classmethod
    def format_printable_price(cls, *args, **kwargs):
        return format_printable_price(*args, **kwargs)

    @property
    def price_values(self):

        fields = [
            'price_wholesale',
            'price_retail',
            'initial_currency',
            'price_usd',
            'price_eur',
            'price_uah'
        ]

        return {field: getattr(self, field) for field in fields}

    class Meta:
        abstract = True


def subscribe_on_exchange_rates(model):
    _MULTI_CURRENCY_MODELS.add(model)
    return model


@register_service('exchange')
def factory(services, user, session, **kwargs):
    return ExchangeService(user, session)
