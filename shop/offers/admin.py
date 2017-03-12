
from django.contrib import admin

from shop.offers.models import ProductPriceOffer


class ProductPriceOfferAdmin(admin.ModelAdmin):

    list_display = (
        'product', 'name', 'mobile', 'email', 'user', 'date_created', 'status',
    )
    list_editable = ('status', )
    search_fields = ('name', 'mobile', 'email', )
    list_filter = ('status', )


admin.site.register(ProductPriceOffer, ProductPriceOfferAdmin)
