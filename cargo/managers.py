
from exchange.managers import MultiCurrencyManager

from cargo.querysets import ProductQuerySet


class ProductManager(MultiCurrencyManager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def visible(self):
        return self.get_queryset().visible()

    def for_category(self, category):
        return self.get_queryset().for_category(category)

    def search(self, **kwargs):
        return self.get_queryset().search(**kwargs)

    def with_attr_values(self, value_ids):
        return self.get_queryset().with_attr_values(value_ids)

    def get_search_fields(self):
        return self.get_queryset().get_search_fields()
