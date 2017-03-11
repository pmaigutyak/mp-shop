
from django.db import models
from django.utils.translation import ugettext_lazy as _

from shop.stock.constants import AVAILABILITY_IN_STOCK, AVAILABILITY_CHOICES


class ProductStockMixin(object):

    availability = models.PositiveSmallIntegerField(
        _('Availability'), choices=AVAILABILITY_CHOICES,
        default=AVAILABILITY_IN_STOCK)

    qty = models.IntegerField(_('Qty'), blank=True, default=1)

    min_qty = models.PositiveIntegerField(_('Min qty'), blank=True, default=0)
