
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
    currency = context.request.session.get(CURRENCY_SESSION_KEY)

    if currency is not None:
        return product.price.convert(currency, printable=True)

    return product.price.printable_default
