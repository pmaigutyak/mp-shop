
from django.apps import apps

__all__ = ['Comparison']


class ComparisonItem(object):

    def __init__(self, product):
        self.product = product

    def __repr__(self):
        return self.product.title

    def to_dict(self):
        return {
            'product_pk': self.product.pk,
            'category_pk': self.product.category_id
        }


class Comparison(object):

    def __init__(self, session, session_key='comparison'):

        self._items_dict = {}

        self.session = session
        self.session_key = session_key

        if self.session_key in self.session:

            representation = self.session[self.session_key]

            ids = representation.keys()

            Product = apps.get_model('products', 'Product')

            for product in Product.objects.filter(pk__in=ids)\
                    .select_related('category'):
                self._items_dict[product.pk] = ComparisonItem(product)

    def __contains__(self, product):
        return product in self.products

    def get_product(self, pk):
        return self._items_dict.get(pk)

    def update_session(self):
        self.session[self.session_key] = self.serialize()
        self.session.modified = True

    def add(self, product):

        if product not in self.products:
            self._items_dict[product.pk] = ComparisonItem(product)
            self.update_session()

    def remove(self, product):
        if product in self.products:
            del self._items_dict[product.pk]
            self.update_session()

    def clear(self):
        self._items_dict = {}
        self.update_session()

    @property
    def items(self):
        return self._items_dict.values()

    @property
    def count(self):
        return len(self._items_dict)


    @property
    def is_empty(self):
        return self.count == 0

    @property
    def products(self):
        return [item.product for item in self.items]

    def get_products(self, category):
        products = []
        for item in self.items:
            if item.product.category.pk == category.pk:
                products.append(item.product)
        return products

    @property
    def categories(self):
        items = []
        for item in self.items:
            if not item.product.category in items:
                items.append(item.product.category)
        return items

    def serialize(self):
        items = {}
        for item in self.items:
            product_id = str(item.product.pk)
            items[product_id] = item.to_dict()
        return items
