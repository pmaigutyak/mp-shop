
from django.apps import apps
from django.db.models import F

from shop.stock.constants import AVAILABILITY_COLORS


def get_endangered_products():
    Product = apps.get_model('products', 'Product')
    return Product.objects.filter(min_qty__gt=F('qty'))


def get_availability_color(availability):
    return AVAILABILITY_COLORS.get(availability)
