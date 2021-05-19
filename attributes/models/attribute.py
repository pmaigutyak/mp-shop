
from django.db import models
from django.conf import settings
from django.forms import CharField, ModelChoiceField
from django.utils.translation import ugettext, ugettext_lazy as _

from ordered_model.models import (
    OrderedModel,
    OrderedModelManager,
    OrderedModelQuerySet)

from attributes.models.attribute_value import AttributeValue, VALUE_FIELDS
from attributes.constants import ATTR_TYPE_SELECT, ATTR_TYPES


class AttributeQuerySet(OrderedModelQuerySet):

    def visible(self):
        return self.filter(is_visible=True)

    def for_filter(self):
        return self.filter(type=ATTR_TYPE_SELECT, is_filter=True)

    def for_categories(self, categories):
        return self.filter(categories__in=categories)


class AttributeManager(OrderedModelManager):

    def get_queryset(self):
        return AttributeQuerySet(self.model, using=self._db)

    def visible(self):
        return self.get_queryset().visible()

    def for_filter(self):
        return self.get_queryset().for_filter()

    def for_categories(self, categories):
        return self.get_queryset().for_categories(categories)


class Attribute(OrderedModel):

    categories = models.ManyToManyField(
        settings.ATTRIBUTES_CATEGORY_MODEL,
        related_name='attributes',
        blank=True,
        verbose_name=_("Categories"))

    name = models.CharField(
        _('Name'),
        max_length=128)

    slug = models.CharField(
        _('Code'),
        max_length=255,
        db_index=True,
        blank=True,
        null=False)

    type = models.PositiveSmallIntegerField(
        choices=ATTR_TYPES,
        default=ATTR_TYPE_SELECT,
        null=False,
        verbose_name=_("Type"))

    is_required = models.BooleanField(
        _('Required'),
        default=False,
        help_text=_('You will not be able to update record without filling '
                    'this field'))

    is_visible = models.BooleanField(
        _('Is visible'),
        default=True,
        help_text=_('Display this attribute for users'))

    is_filter = models.BooleanField(
        _('Is filter'),
        default=False,
        help_text=_('Display this attribute in records filter'))

    objects = AttributeManager()

    @property
    def has_options(self):
        return self.type == ATTR_TYPE_SELECT

    @property
    def full_slug(self):
        return 'attr_' + self.slug

    @property
    def category_ids_str(self):
        ids = self.categories.all().values_list('id', flat=True)
        return ','.join(map(str, ids))

    def __str__(self):
        return self.name

    def get_form_field_label(self):

        label = self.name

        if self.is_required:
            label += ' *'

        return label

    def get_option_form_field_name(self):
        return 'option_' + self.full_slug

    def build_form_fields(self):

        fields = {self.full_slug: self.build_form_field()}

        if self.has_options:
            fields[self.get_option_form_field_name()] = (
                self.build_option_form_field())

        for field in fields.values():
            field.widget.attrs['data-category-ids'] = self.category_ids_str

        return fields

    def build_form_field(self):

        params = {'label': self.get_form_field_label(), 'required': False}

        if self.type is ATTR_TYPE_SELECT:
            params['queryset'] = self.options.all()
            field =  ModelChoiceField(**params)
        else:
            field = VALUE_FIELDS[self.type].formfield(**params)

        return field

    def build_option_form_field(self):
        label = self.name + ugettext(' [New value]')
        return CharField(label=label, required=False)

    def save_value(self, entry, value):

        params = {'entry': entry, 'attr': self}

        if not value:
            AttributeValue.objects.filter(**params).delete()
            return None

        try:
            attr_value = AttributeValue.objects.get(**params)
        except AttributeValue.DoesNotExist:
            attr_value = AttributeValue(**params)

        attr_value.value = value
        attr_value.save()

        return attr_value

    class Meta:
        ordering = ['order']
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attributes')
