
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ProductPriceOffer(models.Model):

    STATUS_NOT_REVIEWED = 'not_reviewed'
    STATUS_PROCESSING = 'processing'
    STATUS_CANCELED = 'canceled'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = (
        (STATUS_NOT_REVIEWED, _('Not reviewed')),
        (STATUS_PROCESSING, _('Processing')),
        (STATUS_CANCELED, _('Canceled')),
        (STATUS_COMPLETED, _('Completed')),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='offers',
        null=True,
        blank=True,
        verbose_name=_('User'),
        on_delete=models.SET_NULL)

    status = models.CharField(
        _('Status'),
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_NOT_REVIEWED)

    product = models.ForeignKey(
        'products.Product',
        related_name='price_offers',
        verbose_name=_("Product"),
        on_delete=models.CASCADE)

    name = models.CharField(
        _("Name"),
        max_length=255,
        blank=False,
        null=False)

    mobile = models.CharField(
        _("Mobile phone"),
        max_length=255,
        blank=False,
        null=False)

    email = models.EmailField(
        _("Email"),
        max_length=255,
        blank=False,
        null=False)

    text = models.TextField(
        _('Offer'),
        blank=False,
        max_length=1000)

    date_created = models.DateTimeField(
        _("Date created"),
        auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'products_priceoffer'
        ordering = ['-date_created']
        verbose_name = _('Product price offer')
        verbose_name_plural = _('Product price offers')
