
from django.utils.translation import ugettext_lazy as _


AVAILABILITY_IN_STOCK = 0
AVAILABILITY_ORDER = 1
AVAILABILITY_NOT_AVAILABLE = 2

AVAILABILITY_CHOICES = (
    (AVAILABILITY_IN_STOCK, _('In stock')),
    (AVAILABILITY_NOT_AVAILABLE, _('Not available')),
    (AVAILABILITY_ORDER, _('Should be ordered')),
)
