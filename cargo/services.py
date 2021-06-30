
from random import randint

from django.apps import apps

from cargo import constants

from model_search import model_search
from modeltranslation.utils import get_translation_fields


class ProductService(object):

    history_product_count = 6
    related_product_count = 6

    SORT_MAP = {
        constants.PRODUCT_ORDER_BY_NEWEST: '-id',
        constants.PRODUCT_ORDER_BY_PRICE_LOW_TO_HIGH: 'price_retail',
        constants.PRODUCT_ORDER_BY_PRICE_HIGH_TO_LOW: '-price_retail',
    }

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

        if 'category' in query:
            queryset = queryset.filter(category=query['category'])

        if 'attr_values' in query and query['attr_values']:
            queryset = queryset.filter(
                attr_values__value_option__in=query['attr_values'])

        if 'query' in query and query['query']:
            queryset = model_search(
                query['query'], queryset, self.get_search_fields())

        order_by = query.get('order_by')

        if order_by:
            queryset = self.order_queryset(queryset, order_by)

        return queryset.set_currency(self._exchange.get_active_currency())

    def get_search_fields(self):
        return (
            ['code'] +
            get_translation_fields('name') +
            get_translation_fields('description')
        )

    def order_queryset(self, queryset, order_by):

        try:
            order_by = self.SORT_MAP[order_by]
        except KeyError:
            pass

        return queryset.order_by(order_by)

    def latest(self):
        return self.filter({
            'is_available': True,
            'order_by': constants.PRODUCT_ORDER_BY_NEWEST
        })

    def add_to_history(self, product_id):

        product_ids = self._session.get('PRODUCT_HISTORY', [])

        if product_id in product_ids:
            product_ids.remove(product_id)

        product_ids.insert(0, product_id)

        self._session['PRODUCT_HISTORY'] = product_ids

    def get_from_history(self, queryset, count=None):

        if count is None:
            count = self.history_product_count

        ids = self._session.get('PRODUCT_HISTORY', [])[:count]

        if not ids:
            return []

        return queryset.filter(id__in=ids)

    def get_related(self, queryset, product_id, count=None):

        if count is None:
            count = self.related_product_count

        index = 0

        related_products = queryset.exclude(pk=product_id)

        products_count = len(related_products)

        if products_count:

            if products_count > count:
                index = randint(0, products_count - count)

            return related_products[index:index + count]

        return []

    def format_printable_price(self, *args, **kwargs):
        return self.product_class.format_printable_price(*args, **kwargs)

    @property
    def product_class(self):
        return apps.get_model('products', 'Product')
