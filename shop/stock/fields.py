
from django.db import models
from django.utils.translation import ugettext_lazy as _

from shop.stock.constants import (
    AVAILABILITY_IN_STOCK, AVAILABILITY_CHOICES)


class ProductAvailabilityField(models.PositiveSmallIntegerField):

    def __init__(self, *args, **kwargs):
        super(ProductAvailabilityField, self).__init__(
            verbose_name=_('Availability'),
            choices=AVAILABILITY_CHOICES,
            default=AVAILABILITY_IN_STOCK)
