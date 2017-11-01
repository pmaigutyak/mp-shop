
from django.apps import apps
from django import template

from shop.currencies.settings import CURRENCY_SESSION_KEY

register = template.Library()


@register.assignment_tag
def get_categories():
    category_model = apps.get_model('products', 'ProductCategory')
    return category_model.objects.all()


@register.assignment_tag
def get_root_categories():
    category_model = apps.get_model('products', 'ProductCategory')
    return category_model.objects.root_nodes()


@register.simple_tag(takes_context=True)
def get_printable_product_price(context, product):

    exchange_rate_model = apps.get_model('currencies', 'ExchangeRate')

    dst_currency = context.request.session.get(CURRENCY_SESSION_KEY)

    if dst_currency is not None:
        return exchange_rate_model.convert(
            product.price.initial, product.currency, int(dst_currency),
            printable=True)

    return product.price.printable_default
