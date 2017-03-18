
from django import forms

from shop.attributes.models import ProductAttributeValue


class SearchProductAttrMixin(object):

    def __init__(self, products, category, *args, **kwargs):

        self._attributes = category.attributes.all()

        super(SearchProductAttrMixin, self).__init__(
            products, category, *args, **kwargs)

        options = self._get_available_options()

        for attr in self._attributes:
            self.fields[attr.full_slug] = self._build_attr_field(attr, options)

    def _filter(self, products):

        products = super(SearchProductAttrMixin, self)._filter(products)

        if not self.data:
            return products

        for attr in self._attributes:

            values = self.data.getlist(attr.full_slug)

            if not values:
                continue

            products = products.filter(
                attribute_values__value_option__in=values)

        return products

    def _build_attr_field(self, attr, available_options):

        choices = [(o.id, o.option) for o in available_options[attr.pk]]

        return forms.MultipleChoiceField(
            widget=forms.CheckboxSelectMultiple, label=attr.name,
            required=False, choices=choices)

    def _get_available_options(self):

        added_options = []

        options = {attr.pk: [] for attr in self._attributes}

        attr_values = ProductAttributeValue.objects.filter(
            attribute__in=self._attributes, product__in=self._products
        ).select_related('value_option')

        for value in attr_values:

            option = value.value_option

            if option not in added_options:
                added_options.append(option)
                options[value.attribute_id].append(option)

        return options