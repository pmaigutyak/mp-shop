
from copy import copy

from exchange.querysets import MultiCurrencyQuerySet

from modeltranslation.utils import get_translation_fields
from model_search import model_search


class ProductQuerySet(MultiCurrencyQuerySet):

    def visible(self):
        return self.filter(is_visible=True)

    def for_category(self, category):
        return self.filter(category=category)

    def search(self, **kwargs):

        queryset = copy(self)

        query = kwargs.get('query')

        if query:
            queryset = model_search(query, queryset, self.get_search_fields())

        return queryset

    def get_search_fields(self):
        return (
            ['code'] +
            get_translation_fields('name') +
            get_translation_fields('description')
        )

    def with_attr_values(self, value_ids):

        if value_ids:
            return self.filter(attr_values__value_option__in=value_ids)

        return self
