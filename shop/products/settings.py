
from django.conf import settings


SHOP_PRODUCT_MODEL = getattr(settings, 'SHOP_PRODUCT_MODEL', None)
