
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ordered_model.models import OrderedModelBase

from shop.lib import get_preview, get_file_upload_path


def get_product_image_upload_path(instance, filename):
    return get_file_upload_path(
        'product_images/%d' % instance.product_id, filename)


class AbstractProductImage(OrderedModelBase):

    product = models.ForeignKey(
        'products.Product', related_name='images', verbose_name=_("Product"))

    file = models.ImageField(
        _("File"), upload_to=get_product_image_upload_path, max_length=255)

    order = models.PositiveIntegerField(_('Ordering'), default=0)

    order_field_name = 'order'
    order_with_respect_to = 'product'

    def __unicode__(self):
        return self.product.title

    @property
    def preview(self):
        return get_preview(self.file)

    preview.fget.short_description = _('Preview')

    class Meta:
        abstract = True
        ordering = ('order', 'id', )
        verbose_name = _('Product image')
        verbose_name_plural = _('Product images')
