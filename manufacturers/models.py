
from django.apps import apps
from django.db import models
from django.utils.translation import ugettext_lazy as _

from manufacturers.signals import manufacturer_replaced


class Manufacturer(models.Model):

    name = models.CharField(
        _('Manufacturer name'),
        max_length=255,
        unique=True,
        db_index=True)

    new_name = models.CharField(
        _('Destination name'),
        max_length=255,
        blank=True)

    logo = models.ImageField(
        _('Logo'),
        max_length=255,
        blank=True,
        null=True,
        upload_to='manufacturers')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_new_name = self.new_name

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        super().save(**kwargs)
        if self.new_name == self._original_new_name:
            return

        if apps.is_installed('celery'):
            self._handle_adjustment_async.delay(self.pk)
        else:
            _handle_adjustment(self.pk)

    if apps.is_installed('celery'):
        from core.celery_app import celery_app

        @staticmethod
        @celery_app.task
        def _handle_adjustment_async(manufacturer_id):
            _handle_adjustment(manufacturer_id)

    class Meta:
        ordering = ['name']
        verbose_name = _('Manufacturer')
        verbose_name_plural = _('Manufacturers')


def _handle_adjustment(manufacturer_id):

    src = Manufacturer.objects.get(id=manufacturer_id)

    dst, created = Manufacturer.objects.get_or_create(name=src.new_name)

    manufacturer_replaced.send(Manufacturer, src_id=src.id, dst_id=dst.id)


class ManufacturerField(models.ForeignKey):

    def __init__(
            self,
            to=Manufacturer,
            on_delete=models.SET_NULL,
            verbose_name=_('Manufacturer'),
            blank=True,
            null=True,
            *args, **kwargs):
        super().__init__(
            to=to,
            on_delete=on_delete,
            verbose_name=verbose_name,
            blank=blank,
            null=null,
            *args, **kwargs)
