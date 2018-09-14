
from django.db import models
from django.utils.translation import ugettext_lazy as _

from shop.attributes.constants import (
    ATTR_TYPE_TEXT, ATTR_TYPE_SELECT, ATTR_TYPES)


class ProductAttrQuerySet(models.QuerySet):

    def visible(self):
        return self.filter(is_visible=True)

    def for_filter(self):
        return self.filter(type=ATTR_TYPE_SELECT, is_filter=True)


class ProductAttrValueManager(models.Manager):

    def get_queryset(self):
        return ProductAttrQuerySet(self.model, using=self._db)

    def visible(self):
        return self.get_queryset().visible()

    def for_filter(self):
        return self.get_queryset().for_filter()


class ProductAttr(models.Model):

    category = models.ForeignKey(
        'products.ProductCategory', related_name='attributes', blank=True,
        null=True, verbose_name=_("Product category"))

    name = models.CharField(_('Name'), max_length=128)

    slug = models.CharField(_('Code'), max_length=255, db_index=True,
                            blank=True, null=False)

    type = models.PositiveSmallIntegerField(
        choices=ATTR_TYPES, default=ATTR_TYPE_TEXT,
        null=False, verbose_name=_("Type"))

    required = models.BooleanField(
        _('Required'), default=False,
        help_text=_('You will not be able to update product without filling '
                    'this field'))

    is_visible = models.BooleanField(
        _('Is visible'), default=True,
        help_text=_('Display this attribute for users'))

    is_filter = models.BooleanField(
        _('Is filter'), default=False,
        help_text=_('Display this attribute in products filter'))

    @property
    def has_options(self):
        return self.type == ATTR_TYPE_SELECT

    @property
    def full_slug(self):
        return 'attr_%s' % self.slug

    def __unicode__(self):
        return self.name

    def save_value(self, product, value):

        value_obj, c = product.attribute_values.get_or_create(attribute=self)

        if value is None or value == '':
            value_obj.delete()
            return

        if value != value_obj.value:
            value_obj.value = value
            value_obj.save()

    class Meta:
        unique_together = ['slug', 'category']
        ordering = ['name']
        verbose_name = _('Product attribute')
        verbose_name_plural = _('Product attributes')
