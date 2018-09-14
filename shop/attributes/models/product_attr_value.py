
from django.db import models
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from shop.attributes.constants import (
    ATTR_TYPE_TEXT, ATTR_TYPE_INT, ATTR_TYPE_BOOL, ATTR_TYPE_SELECT)


ATTR_VALUE_TEXT = models.TextField(_('Text'), blank=True, null=True)
ATTR_VALUE_INT = models.IntegerField(_('Integer'), blank=True, null=True)
ATTR_VALUE_BOOL = models.NullBooleanField(_('Boolean'), blank=True)
ATTR_VALUE_OPTION = models.ForeignKey(
    'products.ProductAttrOption', blank=True, null=True,
    related_name='attr_values', verbose_name=_("Option"))

VALUE_FIELDS = {
    ATTR_TYPE_TEXT: ATTR_VALUE_TEXT,
    ATTR_TYPE_INT: ATTR_VALUE_INT,
    ATTR_TYPE_BOOL: ATTR_VALUE_BOOL,
    ATTR_TYPE_SELECT: ATTR_VALUE_OPTION,
}


class ProductAttrValueQuerySet(models.QuerySet):

    def visible(self):
        return self.filter(attr__is_visible=True)


class ProductAttrValueManager(models.Manager):

    def get_queryset(self):
        return ProductAttrValueQuerySet(self.model, using=self._db)

    def visible(self):
        return self.get_queryset().visible()


class ProductAttrValue(models.Model):

    attr = models.ForeignKey(
        'products.ProductAttr', verbose_name=_("Attribute"),
        related_name='values')

    product = models.ForeignKey(
        'products.Product', verbose_name=_("Product"),
        related_name='attr_values')

    objects = ProductAttrValueManager()

    value_text = ATTR_VALUE_TEXT
    value_int = ATTR_VALUE_INT
    value_bool = ATTR_VALUE_BOOL
    value_option = ATTR_VALUE_OPTION

    @staticmethod
    def get_value_field(field_type):
        return VALUE_FIELDS[field_type]

    @property
    def value_field(self):
        return self.get_value_field(self.attr.type)

    def get_value(self):
        return getattr(self, self.value_field.name)

    def set_value(self, new_value):

        if self.attr.has_options and isinstance(new_value, six.string_types):

            new_value = self.attr.option_group.options.get(
                option=new_value)

        setattr(self, self.value_field.name, new_value)

    value = property(get_value, set_value)

    def as_text(self):

        value = self.get_value()

        if self.attr.type == ATTR_TYPE_BOOL:

            if value is None:
                return ''

            return _('Yes') if value else _('No')

        return unicode('' if value is None else value)

    def as_html(self):
        return self.as_text()

    def __unicode__(self):
        return '{}: {}'.format(self.attr.name, self.as_text())

    class Meta:
        ordering = ('attr__name', )
        unique_together = ('attr', 'product')
        verbose_name = _('Product attribute value')
        verbose_name_plural = _('Product attribute values')
