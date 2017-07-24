
from copy import deepcopy

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from slugify import slugify_url

from modeltranslation.admin import TranslationTabularInline

from shop.attributes.constants import ATTR_TYPE_SELECT
from shop.attributes.models import (
    ProductAttribute, AttributeOption, VALUE_FIELDS)


class ProductAttributeForm(forms.ModelForm):

    def clean_option_group(self):
        data = self.cleaned_data

        option_group = data.get('option_group')

        if data.get('type') == ATTR_TYPE_SELECT and not option_group:
            raise forms.ValidationError(
                _('Option group is required for field type select'))

        return option_group

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')

        if slug:
            return slug

        name = self.cleaned_data.get('name_%s' % settings.LANGUAGE_CODE)
        return slugify_url(name, separator='_')

    class Meta:
        model = ProductAttribute
        fields = '__all__'


class AttributeOptionInline(TranslationTabularInline):

    model = AttributeOption
    extra = 0


class ProductFormMixin(object):

    def __init__(self, *args, **kwargs):

        super(ProductFormMixin, self).__init__(*args, **kwargs)

        if self.instance.pk:
            self._build_attr_fields()

    def get_option_field_name(self, attr):
        return 'option_' + attr.full_slug

    def clean(self):
        data = super(ProductFormMixin, self).clean()

        for attr in self.instance.attr.all():

            if attr.has_options:
                new_option = data.get(self.get_option_field_name(attr))

                if new_option:
                    option, c = attr.option_group.options.get_or_create(
                        option=new_option)
                    data[attr.full_slug] = option

        return data

    def save(self, commit=True):
        product = super(ProductFormMixin, self).save(commit)

        if 'category' in self.changed_data:
            product.attribute_values.all().delete()

        return product

    def _build_attr_fields(self):

        fields = self.fields = deepcopy(self.base_fields)

        for attr in self.instance.attr.all():

            fields[attr.full_slug] = self._build_attr_field(attr)

            if attr.has_options:
                label = attr.name + unicode(_(' [New value]'))
                fields[self.get_option_field_name(attr)] = forms.CharField(
                    label=label, required=False)

            try:
                value = self.instance.attribute_values.get(
                    attribute=attr).value
            except ObjectDoesNotExist:
                pass
            else:
                self.initial[attr.full_slug] = value

    def _post_clean(self):

        for attr in self.instance.attr.all():

            if attr.full_slug in self.cleaned_data:
                value = self.cleaned_data[attr.full_slug]
                setattr(self.instance.attr, attr.slug, value)

        super(ProductFormMixin, self)._post_clean()

    def _build_attr_field(self, attr):

        kwargs = {'label': attr.name, 'required': attr.required}

        if attr.type is ATTR_TYPE_SELECT:
            kwargs['queryset'] = attr.option_group.options.all()
            return forms.ModelChoiceField(**kwargs)

        return VALUE_FIELDS[attr.type].formfield(**kwargs)