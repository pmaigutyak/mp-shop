
from django.db import models
from django.utils.translation import ugettext_lazy as _


class DeliveryMethod(models.Model):

    name = models.CharField(_('Name'), max_length=255)

    code = models.CharField(_('Code'), max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Delivery method')
        verbose_name_plural = _('Delivery methods')


class DeliveryMethodField(models.ForeignKey):

    def __init__(
            self,
            to=DeliveryMethod,
            verbose_name=_('Delivery method'),
            on_delete=models.CASCADE,
            null=True,
            *args, **kwargs):

        super().__init__(
            to,
            verbose_name=verbose_name,
            on_delete=on_delete,
            null=null,
            *args, **kwargs)


class Region(models.Model):

    name = models.CharField(_('Name'), max_length=255)

    reference = models.CharField(_('Reference'), max_length=255)

    def __str__(self):
        if self.reference == '71508128-9b87-11de-822f-000c2965ae0e':
            return self.name

        return '{} {}'.format(self.name, _('region'))

    class Meta:
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')


class City(models.Model):

    region = models.ForeignKey(
        Region,
        verbose_name=_('Region'),
        related_name='cities',
        on_delete=models.CASCADE)

    name = models.CharField(_('Name'), max_length=255)

    reference = models.CharField(_('Reference'), max_length=255)

    def __str__(self):
        return '{} - {}'.format(self.name, self.region)

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')


class Warehouse(models.Model):

    city = models.ForeignKey(
        City,
        verbose_name=_('City'),
        related_name='warehouses',
        on_delete=models.CASCADE)

    delivery_method = models.ForeignKey(
        DeliveryMethod,
        verbose_name=_('Delivery method'),
        on_delete=models.CASCADE)

    name = models.CharField(_('Name'), max_length=255, db_index=True)

    reference = models.CharField(_('Reference'), max_length=255)

    def __str__(self):
        return '{}, {}, {}'.format(self.delivery_method, self.city, self.name)

    class Meta:
        verbose_name = _('Warehouse')
        verbose_name_plural = _('Warehouses')
