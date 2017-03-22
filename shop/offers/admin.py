
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from shop.offers.models import ProductPriceOffer


class ProductPriceOfferAdmin(admin.ModelAdmin):

    list_display = [
        'product', 'name', 'mobile', 'email', 'user', 'date_created', 'status',
        'product_link'
    ]
    list_editable = ['status']
    search_fields = ['name', 'mobile', 'email']
    list_filter = ['status']

    def product_link(self, item):
        return mark_safe('<a href="%s" target="_blank">%s</a>' % (
            item.product.get_absolute_url(), _('View product')))

    product_link.short_description = _('Product')


admin.site.register(ProductPriceOffer, ProductPriceOfferAdmin)
