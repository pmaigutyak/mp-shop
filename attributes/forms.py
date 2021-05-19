
from django import forms
from django.utils.translation import ugettext
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property

from apps.products.models import Product

from attributes.models import (
    Attribute,
    AttributeValue,
    AttributeOption)


class FilterForm(forms.Form):

    def __init__(self, category, *args, **kwargs):

        self._attributes = Attribute\
            .objects\
            .visible()\
            .for_filter()\
            .for_categories([category])

        super().__init__(*args, **kwargs)

        for attr in self._attributes:
            self.fields[attr.full_slug] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple,
                label=attr.name,
                required=False)

    def set_options(self, entries):

        if not entries:
            self.fields = {}
            return

        choices = {attr.id: [] for attr in self._attributes}

        attr_values = AttributeValue.objects.filter(
            attr__in=self._attributes,
            entry__in=entries
        ).values_list('id', flat=True)

        options = AttributeOption\
            .objects\
            .filter(attr_values__in=attr_values)\
            .order_by('name')\
            .distinct()

        for option in options:
            choices[option.attr_id].append((option.id, option, ))

        for attr in self._attributes:
            if choices[attr.id]:
                self.fields[attr.full_slug].choices = choices[attr.id]
            else:
                del self.fields[attr.full_slug]

    def get_value_ids(self):

        ids = []

        for attr in self._attributes:
            ids += self.data.getlist(attr.full_slug)

        return ids

    def _get_available_options(self):

        added_options = []

        options = {attr.pk: [] for attr in self._attributes}

        attr_values = AttributeValue.objects.filter(
            attribute__in=self._attributes,
            entry__in=self._entries
        ).select_related('value_option')

        for value in attr_values:

            option = value.value_option

            if option not in added_options:
                added_options.append(option)
                options[value.attribute_id].append(option)

        return options


class AttributesForm(forms.ModelForm):

    def __init__(
            self,
            data=None,
            files=None,
            instance=None,
            initial=None,
            **kwargs):

        if instance and instance.pk:
            initial = self._get_initial_data(instance)

        super().__init__(
            data=data,
            files=files,
            instance=instance,
            initial=initial,
            **kwargs)

        for attr in self._attributes:

            fields = attr.build_form_fields()

            self.fields.update(fields)

    def _get_initial_data(self, instance):

        initial = {}

        values = {
            v.attr.full_slug: v.get_value()
            for v in AttributeValue.objects.filter(
                attr__in=self._attributes,
                entry=instance
            )
        }

        for attr in self._attributes:
            initial[attr.full_slug] = values.get(attr.full_slug)

        return initial

    def clean(self):

        data = self.cleaned_data

        for attr in self._attributes:

            if attr.has_options:
                new_option = data.get(attr.get_option_form_field_name())

                if new_option:
                    option, c = attr.options.get_or_create(name=new_option)
                    data[attr.full_slug] = option

                if not data.get(attr.full_slug) and attr.is_required:
                    raise ValidationError({
                        attr.full_slug: ugettext('{} is required').format(
                            attr.name)
                    })

        return data

    def commit(self, instance):

        for attr in Attribute.objects.for_categories([instance.category]):

            if attr.full_slug in self.cleaned_data:
                value = self.cleaned_data[attr.full_slug]
                attr.save_value(instance, value)

        return instance

    @cached_property
    def _attributes(self):
        return list(Attribute.objects.all())

    class Media:
        js = ('attrs/form.js', )

    class Meta:
        model = Product
        fields = ['id']
