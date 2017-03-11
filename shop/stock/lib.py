
from django.apps import apps
from django.db.models import F


def get_endangered_products():
    product_model = apps.get_model('products', 'Product')
    return product_model.objects.filter(min_qty__gt=F('qty'))
