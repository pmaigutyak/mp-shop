
from django.db.models import F

from exchange.utils import get_price_factory
from exchange.constants import CURRENCY_NAMES, CURRENCIES
from exchange.models import ExchangeRates, _MULTI_CURRENCY_MODELS


def update_all_prices():

    rates = ExchangeRates.get()

    field = lambda c: 'price_{}'.format(CURRENCY_NAMES[c])

    for src, src_name in CURRENCIES:

        params = {}

        for dst, dst_name in CURRENCIES:
            price_factory = get_price_factory(rates, src, dst)

            params[field(dst)] = price_factory(F('price_retail'))

        for model in _MULTI_CURRENCY_MODELS:

            queryset = model.objects.filter(initial_currency=src)

            queryset.update(
                price_uah=0,
                price_usd=0,
                price_eur=0
            )

            queryset.filter(
                price_retail__gt=0
            ).update(
                **params
            )
