
from django.utils.translation import ugettext_lazy as _


PRODUCT_ORDER_BY_NEWEST = 'newest'
PRODUCT_ORDER_BY_PRICE_HIGH_TO_LOW = '-price'
PRODUCT_ORDER_BY_PRICE_LOW_TO_HIGH = 'price'
PRODUCT_ORDER_BY_A_TO_Z = 'name'
PRODUCT_ORDER_BY_Z_TO_A = '-name'

PRODUCT_ORDER_CHOICES = (
    (PRODUCT_ORDER_BY_NEWEST, _('Newest')),
    (PRODUCT_ORDER_BY_PRICE_HIGH_TO_LOW, _('Price (high-low)')),
    (PRODUCT_ORDER_BY_PRICE_LOW_TO_HIGH, _('Price (low-high)')),
    (PRODUCT_ORDER_BY_A_TO_Z, _('A-Z')),
    (PRODUCT_ORDER_BY_Z_TO_A, _('Z-A')),
)
