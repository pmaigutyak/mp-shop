
from django.apps import apps
from django.db.models import F


def get_endangered_products():
    Product = apps.get_model('products', 'Product')
    return Product.objects.filter(min_qty__gt=F('qty'))
