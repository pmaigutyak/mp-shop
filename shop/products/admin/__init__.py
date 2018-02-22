
from django.apps import apps
from django.conf import settings
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from ckeditor.widgets import CKEditorWidget
from mptt.admin import MPTTModelAdmin
from modeltranslation.admin import TranslationAdmin

from shop.products.settings import (
    IS_CKEDITOR_ENABLED_FOR_PRODUCT_DESCRIPTION)

from shop.currencies.settings import CURRENCIES
from shop.currencies.models import ExchangeRate

from shop.products.admin.forms import ProductForm, ProductImageInline
from shop.products.admin import views
from shop.products.admin import actions

from shop.lib import get_show_on_site_link


class ProductAdmin(TranslationAdmin):

    inlines = [ProductImageInline]

    actions = [actions.refresh_products_logos]

    form = ProductForm

    list_display = [
        'id', 'title', 'category', 'printable_price', 'code', 'date_updated',
        'get_show_link', 'preview'
    ]

    list_display_links = ('title', )

    list_filter = ('category', )

    ordering = ['-id']

    search_fields = apps.get_model('products', 'Product').get_search_fields()

    def __init__(self, *args, **kwargs):

        if IS_CKEDITOR_ENABLED_FOR_PRODUCT_DESCRIPTION:
            self.formfield_overrides = {
                models.TextField: {'widget': CKEditorWidget}
            }

        super(ProductAdmin, self).__init__(*args, **kwargs)

    def get_show_link(self, item):
        return get_show_on_site_link(item.get_absolute_url())

    get_show_link.short_description = _('Show on site')

    def printable_price(self, item):

        html = '<b>%s</b><br />' % item.price.printable_initial

        for currency_id, currency_name in CURRENCIES:
            if currency_id is item.currency:
                continue

            price = str(ExchangeRate.convert(
                item.price.initial, item.currency, currency_id,
                format_price=True))

            html += '<small>%s %s</small> <br />' % (price, currency_name)

        return mark_safe(html)

    printable_price.short_description = _('Price')

    def save_model(self, request, obj, form, change):

        self._product = product = form.save()

        images = form.cleaned_data.get('images', [])

        for image in images:
            if image:
                product.images.create(file=image)

    def save_related(self, request, form, formsets, change):
        super(ProductAdmin, self).save_related(request, form, formsets, change)
        self._product.refresh_logo()


class ProductCategoryAdmin(MPTTModelAdmin, TranslationAdmin):

    list_display = ('full_name', 'product_count', 'preview', )

    def __init__(self, *args, **kwargs):

        self.formfield_overrides = {
            models.TextField: {'widget': CKEditorWidget}
        }

        super(ProductCategoryAdmin, self).__init__(*args, **kwargs)

    def product_count(self, item):
        return item.products.count()

    product_count.short_description = _('Product count')


if 'shop.products' in settings.INSTALLED_APPS:
    from shop.products.models import Product, ProductCategory

    admin.site.register(Product, ProductAdmin)
    admin.site.register(ProductCategory, ProductCategoryAdmin)
