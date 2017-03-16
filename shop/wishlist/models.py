
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class WishListItem(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='wishlist_items',
        verbose_name=_('Owner'))

    product = models.ForeignKey(
        'products.Product', verbose_name=_('Product'),
        on_delete=models.SET_NULL, blank=True, null=True)

    qty = models.PositiveIntegerField(_('Quantity'), default=1)

    product_title = models.CharField(_("Product title"), max_length=255)

    date_created = models.DateTimeField(
        _('Date created'), auto_now_add=True, editable=False)

    def __unicode__(self):
        return self.product.title

    class Meta:
        ordering = ['pk']
        unique_together = (('user', 'product'), )
        verbose_name = _('Wish list item')
        verbose_name_plural = _('Wish list items')