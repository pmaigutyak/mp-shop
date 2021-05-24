
from random import randint

from django.apps import apps


class ProductService(object):

    def __init__(self, services, user, session):
        self._exchange = services.exchange
        self._user = user
        self._session = session

    def filter(self, query={}):

        queryset = self.product_class.objects.all()

        if 'id' in query:
            queryset = queryset.filter(id=query['id'])

        if 'is_visible' in query:
            queryset = queryset.filter(is_visible=query['is_visible'])

        if 'id__in' in query:
            queryset = queryset.filter(id__in=query['id__in'])

        return queryset.set_currency(self._exchange.get_active_currency())

    def latest(self):
        return self.filter({'is_available': True}).order_by('-id')

    def add_to_history(self, product_id):

        product_ids = self._session.get('PRODUCT_HISTORY', [])

        if product_id in product_ids:
            product_ids.remove(product_id)

        product_ids.insert(0, product_id)

        self._session['PRODUCT_HISTORY'] = product_ids

    def get_from_history(self, queryset, count=6):

        ids = self._session.get('PRODUCT_HISTORY', [])[:count]

        if not ids:
            return []

        return queryset.filter(id__in=ids)

    def get_related(self, queryset, product_id, count=6):

        index = 0

        related_products = queryset.exclude(pk=product_id)

        related_products_count = len(related_products)

        if related_products_count:

            if related_products_count > count:
                index = randint(0, related_products_count - count)

            return related_products[index:index + count]

        return []

    def format_printable_price(self, *args, **kwargs):
        return self.product_class.format_printable_price(*args, **kwargs)

    @property
    def product_class(self):
        return apps.get_model('products', 'Product')
