
import re

from exchange.constants import (
    CURRENCIES,
    CURRENCY_NAMES,
    DEFAULT_CURRENCY,
    CURRENCY_EUR,
    CURRENCY_UAH,
    CURRENCY_USD,
    CURRENCY_SESSION_KEY)


def round_number(value, decimal_places=2, down=False):

    assert decimal_places > 0
    factor = 1.0 ** decimal_places
    sign = -1 if value < 0 else 1
    return int(value * factor + sign * (0 if down else 0.5)) / factor


def format_number(value):

    append_comma = lambda match_object: "%s," % match_object.group(0)

    value = "%.2f" % float(value)
    value = re.sub("(\d)(?=(\d{3})+\.)", append_comma, value)

    return value


def format_price(price, round_price=False):
    price = float(price)
    return format_number(round_number(price) if round_price else price)


def format_printable_price(price, currency=DEFAULT_CURRENCY):
    return '%s %s' % (format_price(price), dict(CURRENCIES)[currency])


def get_currency_from_session(session):
    currency = session.get(CURRENCY_SESSION_KEY) or DEFAULT_CURRENCY
    return int(currency)


def get_price_factory(rates, src, dst):

    if src == dst:
        return lambda p: p

    name = lambda c: CURRENCY_NAMES[c]

    if src == CURRENCY_UAH:
        return lambda p: p / getattr(rates, name(dst))

    if dst == CURRENCY_UAH:
        return lambda p: p * getattr(rates, name(src))

    if src == CURRENCY_USD and dst == CURRENCY_EUR:
        return lambda p: p * rates.usd_eur

    if src == CURRENCY_EUR and dst == CURRENCY_USD:
        return lambda p: p / rates.usd_eur

    raise ValueError('Unknown currencies')
