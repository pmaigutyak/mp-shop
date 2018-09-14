
from django.db import models
from django.utils.translation import ugettext_lazy as _

from shop.attributes.models import ProductAttr, ProductAttributes


class ProductCategoryAttrMixin(object):

    def get_attributes(self):
        return ProductAttr.objects.filter(
            models.Q(category=self) | models.Q(category__isnull=True))


class ProductAttrMixin(object):

    attributes = models.ManyToManyField(
        'attributes.ProductAttr', through='ProductAttrValue',
        verbose_name=_("Attributes"))

    def __init__(self, *args, **kwargs):

        super(ProductAttrMixin, self).__init__(*args, **kwargs)

        self.attrs = ProductAttributes(self)

    def save(self, *args, **kwargs):

        is_new = bool(not self.pk)

        super(ProductAttrMixin, self).save(*args, **kwargs)

        if not is_new:
            self.attrs.save()