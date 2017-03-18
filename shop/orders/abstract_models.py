
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator

from shop.currencies.lib import format_printable_price
from shop.orders.settings import (
    ORDER_DELIVERY_METHODS, ORDER_PAYMENT_METHODS, ORDER_STATUSES,
    DEFAULT_STATUS, DEFAULT_DELIVERY_METHOD, DEFAULT_PAYMENT_METHOD
)


class AbstractOrder(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='order',
        verbose_name=_('Customer'), null=True, blank=True)

    payment_method = models.PositiveIntegerField(
        _('Payment method'), null=False,
        blank=DEFAULT_PAYMENT_METHOD is not None,
        choices=ORDER_PAYMENT_METHODS,
        default=DEFAULT_PAYMENT_METHOD
    )

    delivery_method = models.PositiveIntegerField(
        _('Delivery method'), null=False,
        blank=DEFAULT_DELIVERY_METHOD is not None,
        choices=ORDER_DELIVERY_METHODS,
        default=DEFAULT_DELIVERY_METHOD
    )

    status = models.PositiveIntegerField(
        _('Status'), null=False, choices=ORDER_STATUSES,
        default=DEFAULT_STATUS)

    name = models.CharField(
        _("Name, Surname"), max_length=255, blank=False, null=False)

    post_office = models.CharField(
        _("Address and number of post office"),
        max_length=255, blank=True, null=True)

    mobile = models.CharField(
        _("Mobile phone"), max_length=255, blank=False, null=False)

    email = models.EmailField(
        _("Email"), max_length=255, blank=False, null=False)

    date_created = models.DateTimeField(
        _('Date created'), auto_now_add=True, editable=False)

    comment = models.TextField(
        _('Comment'), max_length=1000, blank=True, default='')

    @property
    def printable_name(self):
        return _('Order #%s') % self.id

    def __unicode__(self):
        return self.printable_name

    @property
    def product_count(self):
        return sum([item.qty for item in self.products.all()])

    @property
    def default_total(self):
        return sum([item.default_subtotal for item in self.products.all()])

    @property
    def printable_default_total(self):
        return format_printable_price(self.default_total)

    class Meta:
        abstract = True
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class AbstractOrderProduct(models.Model):

    order = models.ForeignKey(
        'orders.Order', related_name='products', verbose_name=_('Order'))

    parent = models.ForeignKey(
        'products.Product', verbose_name=_('Product'),
        on_delete=models.SET_NULL, blank=True, null=True)

    title = models.CharField(_("Product title"), max_length=255, blank=True)

    price = models.FloatField(_('Price (uah)'), blank=False, null=False)

    qty = models.PositiveIntegerField(
        _('Quantity'), default=1, validators=[MinValueValidator(1)])

    @property
    def order_name(self):
        return self.order.printable_name

    @property
    def default_subtotal(self):
        return self.parent.price.default * self.qty

    @property
    def printable_default_price(self):
        return format_printable_price(self.parent.price.default)

    @property
    def printable_default_subtotal(self):
        return format_printable_price(self.default_subtotal)

    @property
    def code(self):
        if self.parent:
            return self.parent.code

        return ''

    @property
    def product_title(self):
        if self.parent:
            return self.parent.title

        return self.title

    def __unicode__(self):
        return self.product_title

    class Meta:
        abstract = True
        verbose_name = _('Order product')
        verbose_name_plural = _('Order products')