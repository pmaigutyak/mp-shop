
from django import forms

from django_filters import MultipleChoiceFilter

from shop.attributes.models import ProductAttributeValue


class ProductAttrFilterMixin(object):

    def __init__(self, category, *args, **kwargs):

        self._category = category

        super(ProductAttrFilterMixin, self).__init__(*args, **kwargs)

        for attr in self._category.attributes:
            self.filters[attr.full_slug] = self.build_attr_filter(attr)

    def build_attr_filter(self, attr):

        choices = [(o.pk, o.option) for o in self.available_options[attr.pk]]

        attr_filter = MultipleChoiceFilter(
            widget=forms.CheckboxSelectMultiple, label=attr.name,
            required=False, choices=choices, method='filter_attr_option')

        attr_filter.model = self._meta.model
        attr_filter.parent = self

        return attr_filter

    @property
    def available_options(self):

        if not hasattr(self, '_available_options'):

            added_options = []

            options = {attr.pk: [] for attr in self._category.attributes}

            attr_values = ProductAttributeValue.objects.filter(
                attribute__in=self._category.attributes
            ).select_related('value_option')

            for value in attr_values:

                option = value.value_option

                if option not in added_options:

                    added_options.append(option)
                    options[value.attribute_id].append(option)

            self._available_options = options

        return self._available_options

    @property
    def qs(self):
        categories = self._category.get_descendants(include_self=True)
        qs = super(ProductAttrFilterMixin, self).qs
        return qs.filter(category__in=categories)

    def filter_attr_option(self, queryset, name, value):
        return queryset.filter(attribute_values__value_option__in=value)
