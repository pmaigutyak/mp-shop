
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from exchange.models import format_printable_price, MultiCurrencyPrice
from delivery.models import DeliveryMethodField

from orders.constants import (
    PAYMENT_METHODS,
    ORDER_STATUSES,
    ORDER_STATUS_NEW,
    CLOTHES_FIELDS
)


class Order(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='orders',
        verbose_name=_('Owner'), null=True, blank=True,
        on_delete=models.SET_NULL)

    status = models.CharField(
        _('Status'),
        max_length=100,
        choices=ORDER_STATUSES,
        default=ORDER_STATUS_NEW)

    payment_method = models.CharField(
        _('Payment method'),
        max_length=100,
        choices=PAYMENT_METHODS)

    delivery = DeliveryMethodField()

    first_name = models.CharField(_('First name'), max_length=255)

    last_name = models.CharField(_('Last name'), max_length=255)

    middle_name = models.CharField(
        _('Middle name'), max_length=255, blank=True)

    address = models.CharField(_('Address'), max_length=255, blank=True)

    mobile = models.CharField(_('Mobile number'), max_length=255)

    created = models.DateTimeField(
        _('Date created'), auto_now_add=True, editable=False)

    comment = models.TextField(_('Comment'), max_length=1000, blank=True)

    def __str__(self):
        return self.printable_name

    @property
    def printable_name(self):
        return '{} #{}'.format(_('Order'), self.id)

    @property
    def full_name(self):
        return '{} {} {}'.format(
            self.last_name, self.first_name, self.middle_name)

    @property
    def total(self):
        return sum([i.subtotal for i in self.items.all()])

    @property
    def printable_total(self):
        return format_printable_price(self.total)

    @property
    def delivery_method(self):
        return self.delivery.name

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class OrderedProduct(MultiCurrencyPrice):

    order = models.ForeignKey(
        Order,
        verbose_name=_('Order'),
        related_name='items',
        on_delete=models.CASCADE)

    product = models.ForeignKey(
        'products.Product',
        verbose_name=_('Product'),
        related_name='order_items',
        on_delete=models.CASCADE)

    qty = models.PositiveIntegerField(_('Quantity'), default=1)

    def __str__(self):
        return str(self.product)

    @property
    def subtotal(self):
        return self.price * self.qty

    def printable_subtotal(self):
        return format_printable_price(self.subtotal)

    class Meta:
        verbose_name = _('Ordered product')
        verbose_name_plural = _('Ordered products')


class ClothesSize(models.Model):

    MALE_SIZES = (
        (44, '44 (S)'),
        (46, '46 (M)'),
        (48, '48 (M)'),
        (50, '50 (L)'),
        (52, '52 (XL)'),
        (54, '54 (XXL)'),
        (56, '56 (XXL)'),
        (58, '58 (XXL)'),
        (60, '60 (XXXL)'),
        (62, '62 (XXXL)'),
    )

    FEMALE_SIZES = (
        (42, '42 (S)'),
        (44, '44 (M)'),
        (46, '46 (M)'),
        (48, '48 (L)'),
        (50, '50 (XL)'),
        (52, '52 (XXL)'),
        (54, '54 (XXL)'),
        (56, '56 (XXL)'),
        (58, '58 (XXXL)'),
        (60, '60 (XXXL)'),
    )

    SIZE_CHOICES = MALE_SIZES + FEMALE_SIZES

    size = models.IntegerField(
        _('Size'),
        choices=SIZE_CHOICES)

    ordered_product = models.ForeignKey(
        OrderedProduct,
        verbose_name=_('Ordered product'),
        related_name='clothe_sizes',
        on_delete=models.CASCADE)

    breast_size = models.IntegerField(
        _('Breast size'),
        blank=True,
        null=True)

    waist_volume = models.IntegerField(
        _('Waist volume'),
        blank=True,
        null=True)

    hips_volume = models.IntegerField(
        _('Hips volume'),
        blank=True,
        null=True)

    sleeve_length = models.IntegerField(
        _('Length of the sleeve from the shoulder'),
        blank=True,
        null=True)

    shoulder_length = models.IntegerField(
        _('Shoulder length'),
        blank=True,
        null=True)

    product_length = models.IntegerField(
        _('Product length'),
        blank=True,
        null=True)

    back_width = models.IntegerField(
        _('Back width'),
        blank=True,
        null=True)

    neck_volume = models.IntegerField(
        _('Neck volume'),
        blank=True,
        null=True)

    length_of_dress_up_to_waist = models.IntegerField(
        _('Length of dress up to waist'), blank=True, null=True)

    length_of_dress_from_waist = models.IntegerField(
        _('Length of dress from waist'), blank=True, null=True)

    def get_values(self):
        values = []
        for f_name in CLOTHES_FIELDS:
            values.append((
                self._meta.get_field(f_name).verbose_name,
                getattr(self, f_name)
            ), )
        return values
