
import six

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from attributes.managers import AttributeValueManager
from attributes.constants import (
    ATTR_TYPE_TEXT,
    ATTR_TYPE_INT,
    ATTR_TYPE_BOOL,
    ATTR_TYPE_SELECT)


ATTR_VALUE_TEXT = models.TextField(blank=True, null=True)

ATTR_VALUE_INT = models.IntegerField(blank=True, null=True)

ATTR_VALUE_BOOL = models.NullBooleanField(blank=True)

ATTR_VALUE_OPTION = models.ForeignKey(
    'attributes.AttributeOption',
    blank=True,
    null=True,
    related_name='attr_values',
    on_delete=models.SET_NULL)

VALUE_FIELDS = {
    ATTR_TYPE_TEXT: ATTR_VALUE_TEXT,
    ATTR_TYPE_INT: ATTR_VALUE_INT,
    ATTR_TYPE_BOOL: ATTR_VALUE_BOOL,
    ATTR_TYPE_SELECT: ATTR_VALUE_OPTION,
}


class AttributeValue(models.Model):

    attr = models.ForeignKey(
        'attributes.Attribute',
        related_name='values',
        on_delete=models.CASCADE)

    entry = models.ForeignKey(
        settings.ATTRIBUTES_ENTRY_MODEL,
        related_name='attr_values',
        on_delete=models.CASCADE)

    objects = AttributeValueManager()

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

            new_value = self.attr.options.get(option=new_value)

        setattr(self, self.value_field.name, new_value)

    value = property(get_value, set_value)

    def as_text(self):

        value = self.get_value()

        if self.attr.type == ATTR_TYPE_BOOL:

            if value is None:
                return ''

            return _('Yes') if value else _('No')

        return str('' if value is None else value)

    def as_html(self):
        return self.as_text()

    def __str__(self):
        return '{}: {}'.format(self.attr.name, self.as_text())

    class Meta:
        ordering = ('attr__order', )
        unique_together = ('attr', 'entry')
