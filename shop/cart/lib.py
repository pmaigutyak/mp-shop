
from django.apps import apps

from shop.currencies.lib import format_printable_price


CART_SESSION_KEY = 'CART'


class CartItem(object):

    def __init__(self, product, qty):
        self.product = product
        self.qty = int(qty)

    def serialize(self):

        product = self.product

        return {
            'product_pk': product.pk,
            'qty': self.qty,
            'price': str(product.price_in_currency),
            'currency': str(product.currency)
        }

    @property
    def default_subtotal(self):
        return self.product.price.default * self.qty

    @property
    def printable_default_subtotal(self):
        return format_printable_price(self.default_subtotal)

    @property
    def initial_subtotal(self):
        return self.product.price.initial * self.qty

    @property
    def printable_initial_subtotal(self):
        return format_printable_price(
            self.initial_subtotal, currency=self.product.currency)


class Cart(object):

    def __init__(self, session, session_key=None):
        self._items = {}
        self.session = session
        self.session_key = session_key or CART_SESSION_KEY

        if self.session_key in self.session:
            cart_representation = self.session[self.session_key]

            ids_in_cart = cart_representation.keys()

            Product = apps.get_model('products', 'Product')

            for product in Product.objects.filter(pk__in=ids_in_cart):
                item = cart_representation[str(product.pk)]
                self._items[product.pk] = CartItem(product, item['qty'])

    def update_session(self):
        self.session[self.session_key] = self.serialize()
        self.session.modified = True

    def add(self, product, qty=1):

        qty = int(qty)

        if qty < 1:
            raise ValueError('Quantity must be at least 1 when adding to cart')

        if product in self.products:
            self._items[product.pk].qty += qty
        else:
            self._items[product.pk] = CartItem(product, qty)

        self.update_session()

    def remove(self, product):
        if product in self.products:
            del self._items[product.pk]
            self.update_session()

    def clear(self):
        self._items = {}
        self.update_session()

    def set_qty(self, product, qty):
        qty = int(qty)

        if qty < 0:
            raise ValueError('qty must be positive when updating cart')

        if product in self.products:
            self._items[product.pk].qty = qty

            if self._items[product.pk].qty < 1:
                del self._items[product.pk]

            self.update_session()

    def serialize(self):

        obj = {}

        for item in self.items:
            product_id = str(item.product.pk)
            obj[product_id] = item.serialize()

        return obj

    def get_item(self, product):
        return self._items[product.pk]

    @property
    def items(self):
        return self._items.values()

    @property
    def count(self):
        return sum([item.qty for item in self.items])

    @property
    def unique_count(self):
        return len(self._items)

    @property
    def is_empty(self):
        return self.unique_count == 0

    @property
    def products(self):
        return [item.product for item in self.items]

    @property
    def default_total(self):
        return sum([item.default_subtotal for item in self.items])

    @property
    def printable_default_total(self):
        return format_printable_price(self.default_total)

    @property
    def initial_total(self):

        total = {}

        for item in self.items:

            currency = item.product.currency

            if currency in total:
                total[currency] += item.initial_subtotal
            else:
                total[currency] = item.initial_subtotal

        return total

    @property
    def printable_initial_total(self):

        totals = []

        for currency, price in self.initial_total.items():
            totals.append(format_printable_price(price, currency=currency))

        return ', '.join(totals)
