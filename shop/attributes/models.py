
from django.db import models
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from shop.attributes.constants import (
    ATTR_TYPE_BOOL, ATTR_TYPE_INT, ATTR_TYPE_TEXT, ATTR_TYPE_SELECT, ATTR_TYPES
)


ATTR_VALUE_TEXT = models.TextField(_('Text'), blank=True, null=True)
ATTR_VALUE_INT = models.IntegerField(_('Integer'), blank=True, null=True)
ATTR_VALUE_BOOL = models.NullBooleanField(_('Boolean'), blank=True)
ATTR_VALUE_OPTION = models.ForeignKey(
    'attributes.AttributeOption', blank=True, null=True,
    verbose_name=_("Value option"))

VALUE_FIELDS = {
    ATTR_TYPE_TEXT: ATTR_VALUE_TEXT,
    ATTR_TYPE_INT: ATTR_VALUE_INT,
    ATTR_TYPE_BOOL: ATTR_VALUE_BOOL,
    ATTR_TYPE_SELECT: ATTR_VALUE_OPTION,
}


class AttributeOptionGroup(models.Model):

    name = models.CharField(_('Name'), max_length=128)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Attribute option group')
        verbose_name_plural = _('Attribute option groups')


class AttributeOption(models.Model):

    group = models.ForeignKey(
        'attributes.AttributeOptionGroup', related_name='options',
        verbose_name=_("Group"))

    option = models.CharField(_('Option'), max_length=255)

    def __unicode__(self):
        return self.option

    class Meta:
        unique_together = ('group', 'option')
        verbose_name = _('Attribute option')
        verbose_name_plural = _('Attribute options')


class ProductAttribute(models.Model):

    category = models.ForeignKey(
        'products.ProductCategory', related_name='attributes', blank=True,
        null=True, verbose_name=_("Product category"))

    name = models.CharField(_('Name'), max_length=128)

    slug = models.CharField(_('Code'), max_length=255, db_index=True,
                            blank=True, null=False)

    type = models.PositiveSmallIntegerField(
        choices=ATTR_TYPES, default=ATTR_TYPE_TEXT,
        null=False, verbose_name=_("Type"))

    option_group = models.OneToOneField(
        'attributes.AttributeOptionGroup', blank=True, null=True,
        related_name='attribute', verbose_name=_("Option Group"),
        help_text=_('Select an option group if using type "Option"'))

    required = models.BooleanField(_('Required'), default=False)

    is_filter = models.BooleanField(_('Is filter'), default=False)

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
        ordering = ['slug']
        verbose_name = _('Product attribute')
        verbose_name_plural = _('Product attributes')


class ProductAttributeValue(models.Model):

    attribute = models.ForeignKey(
        'attributes.ProductAttribute', verbose_name=_("Attribute"),
        related_name='values')

    product = models.ForeignKey(
        'products.Product', related_name='attribute_values',
        verbose_name=_("Product"))

    value_text = ATTR_VALUE_TEXT
    value_int = ATTR_VALUE_INT
    value_bool = ATTR_VALUE_BOOL
    value_option = ATTR_VALUE_OPTION

    @staticmethod
    def get_value_field(field_type):
        return VALUE_FIELDS[field_type]

    @property
    def value_field(self):
        return self.get_value_field(self.attribute.type)

    def get_value(self):
        return getattr(self, self.value_field.name)

    def set_value(self, new_value):

        if self.attribute.has_options and \
                isinstance(new_value, six.string_types):

            new_value = self.attribute.option_group.options.get(
                option=new_value)

        setattr(self, self.value_field.name, new_value)

    value = property(get_value, set_value)

    def as_text(self):
        value = self.get_value()

        if self.attribute.type == ATTR_TYPE_BOOL:
            if value is None:
                return ''
            return _('Yes') if value else _('No')

        return unicode('' if value is None else value)

    def as_html(self):
        return self.as_text()

    def __unicode__(self):
        return u"%s: %s" % (self.attribute.name, self.as_text())

    class Meta:
        ordering = ('attribute__name', )
        unique_together = ('attribute', 'product')
        verbose_name = _('Product attribute value')
        verbose_name_plural = _('Product attribute values')


class ProductAttrsContainer(object):

    def __setstate__(self, state):
        self.__dict__ = state
        self.initialised = False

    def __init__(self, product):
        self.product = product
        self.initialised = False
        self._attrs = None

    def __getattr__(self, name):
        if not name.startswith('_') and not self.initialised:
            values = self.get_values().select_related('attribute')
            for v in values:
                setattr(self, v.attribute.slug, v.value)
            self.initialised = True
            return getattr(self, name)
        return None

    def get_values(self):
        return self.product.attribute_values.all()

    def get_value_by_attribute(self, attribute):
        return self.get_values().get(attribute=attribute)

    def all(self):
        if not self.product.pk:
            return []

        if not self._attrs:
            self._attrs = self.product.category.get_attributes()

        return self._attrs

    def get_attribute_by_code(self, code):
        return self.all().get(code=code)

    def __iter__(self):
        return iter(self.get_values())

    def save(self):
        for attribute in self.all():
            if hasattr(self, attribute.slug):
                value = getattr(self, attribute.slug)
                attribute.save_value(self.product, value)


class ProductCategoryAttrsMixin(object):

    def get_attributes(self):
        return ProductAttribute.objects.filter(
            models.Q(category=self) | models.Q(category__isnull=True))


class ProductAttrsMixin(object):

    attributes = models.ManyToManyField(
        'attributes.ProductAttribute', through='ProductAttributeValue',
        verbose_name=_("Attributes"))

    def __init__(self, *args, **kwargs):

        super(ProductAttrsMixin, self).__init__(*args, **kwargs)

        self.attr = ProductAttrsContainer(self)

    def save(self, *args, **kwargs):

        is_new = bool(not self.pk)

        super(ProductAttrsMixin, self).save(*args, **kwargs)

        if not is_new:
            self.attr.save()
