
from django.apps import apps
from django import forms
from django.utils.translation import ugettext_lazy as _

from model_search import model_search


class SearchProductForm(forms.Form):

    ORDER_BY_PRICE_HIGH_TO_LOW = 'price'
    ORDER_BY_PRICE_LOW_TO_HIGH = '-price'
    ORDER_BY_NEWEST = 'newest'
    ORDER_BY_A_TO_Z = 'title'
    ORDER_BY_Z_TO_A = '-title'

    ORDER_CHOICES = (
        (ORDER_BY_NEWEST, _('Newest')),
        (ORDER_BY_PRICE_HIGH_TO_LOW, _('Price (high-low)')),
        (ORDER_BY_PRICE_LOW_TO_HIGH, _('Price (low-high)')),
        (ORDER_BY_A_TO_Z, _('A-Z')),
        (ORDER_BY_Z_TO_A, _('Z-A')),
    )

    query = forms.CharField(label=_('Query'), required=False)

    order_by = forms.ChoiceField(
        label=_('Order by'), required=False, choices=ORDER_CHOICES,
        initial=ORDER_BY_NEWEST)

    def __init__(self, products, category=None, *args, **kwargs):
        super(SearchProductForm, self).__init__(*args, **kwargs)

        self._category = category

        if self.is_valid():
            products = self._filter(products)
            products = self._order(products)
        else:
            products = []

        self._products = products

    def _filter(self, products):

        if self._category is not None:
            categories = self._category.get_descendants(include_self=True)
            products = products.filter(category__in=categories)

        query = self.cleaned_data.get('query')

        if query:
            Product = apps.get_model('products', 'Product')
            products = model_search(query, products, Product.get_search_fields())

        return products

    def _order(self, products):

        order_by = self.cleaned_data.get('order_by')

        if not order_by:
            return products

        if order_by == self.ORDER_BY_NEWEST:
            return products.order_by('-id')

        if order_by == self.ORDER_BY_A_TO_Z:
            return products.order_by('title')

        if order_by == self.ORDER_BY_Z_TO_A:
            return products.order_by('-title')

        if order_by == self.ORDER_BY_PRICE_HIGH_TO_LOW:
            return sorted(products, key=lambda p: p.price.default,
                          reverse=True)

        if order_by == self.ORDER_BY_PRICE_LOW_TO_HIGH:
            return sorted(products, key=lambda p: p.price.default)

    def get_objects(self):
        return self._products
