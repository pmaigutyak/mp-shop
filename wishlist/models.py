
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from wishlist import exceptions


class WishListItem(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='wishlist_items',
        verbose_name=_('Owner'), on_delete=models.CASCADE)

    product = models.ForeignKey(
        'products.Product', verbose_name=_('Product'),
        on_delete=models.CASCADE)

    date_created = models.DateTimeField(
        _('Date created'), auto_now_add=True, editable=False)

    def __str__(self):
        return str(self.product)

    class Meta:
        unique_together = ['user', 'product']
        verbose_name = _('Wish list item')
        verbose_name_plural = _('Wish list items')


class WishList(object):

    def __init__(self, user):
        self._user = user

    @property
    def _items(self):

        if not self._user.is_authenticated:
            raise exceptions.UserIsNotAuthenticated()

        if not hasattr(self, '_items_cache'):
            self._items_cache = {
                i.product_id: i for i in
                self._user.wishlist_items.all().select_related('product')
            }

        return self._items_cache

    def add(self, product):

        if product.id in self._items:
            raise exceptions.ProductAlreadyAdded()

        item = self._user.wishlist_items.create(product=product)

        self._items_cache[product.id] = item

    def remove(self, product_id):

        if product_id not in self._items:
            raise exceptions.ItemDoesNotExists()

        self._items[product_id].delete()

        del self._items[product_id]

    def has_product(self, product_id):

        if not self._user.is_authenticated:
            return False

        return product_id in self._items

    def __iter__(self):
        return iter(self._items.values())

    def __len__(self):

        if self._user.is_authenticated:
            return len(self._items)

        return 0
