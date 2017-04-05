
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


def get_preview(img):
    from sorl.thumbnail import get_thumbnail

    try:
        url = get_thumbnail(img, '100x100', crop='center', quality=99).url
    except Exception:
        url = '%s/img/error.png' % settings.STATIC_URL

    return mark_safe('<img src="%s" style="width: 60px;" />' % url)


class ProductAdmin(TranslationAdmin):

    inlines = [ProductImageInline]

    form = ProductForm

    list_display = [
        'id', 'title', 'category', 'printable_price', 'code', 'date_updated',
        'link', 'preview'
    ]

    list_display_links = ('title', )

    list_filter = ('category', )

    search_fields = apps.get_model('products', 'Product').get_search_fields()

    def __init__(self, *args, **kwargs):
        if IS_CKEDITOR_ENABLED_FOR_PRODUCT_DESCRIPTION:
            self.formfield_overrides = {
                models.TextField: {'widget': CKEditorWidget}
            }

        super(ProductAdmin, self).__init__(*args, **kwargs)

    def preview(self, item):

        if not item.logo:
            return '----'

        img_tag = get_preview(item.logo.file)

        template = '<a href="%s" class="preview">%s</a>'

        return mark_safe(template % (item.logo.file.url, img_tag))

    preview.short_description = _('Preview')

    def link(self, item):
        return mark_safe('<a href="%s" target="_blank">%s</a>' % (
            item.get_absolute_url(), _('View')))

    link.short_description = _('Link')

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


class ProductCategoryAdmin(MPTTModelAdmin, TranslationAdmin):

    list_display = ('full_name', 'product_count', 'preview', )

    def product_count(self, item):
        return item.products.count()

    product_count.short_description = _('Product count')

    def preview(self, item):

        if not item.logo:
            return '----'

        return get_preview(item.logo.file)

    preview.short_description = _('Preview')


admin.site.register_view(
    path='products/product-statistic/', view=views.product_statistic,
    urlname='product-statistic')

if 'shop.products' in settings.INSTALLED_APPS:
    import shop.products.translation
    from shop.products.models import Product, ProductCategory

    admin.site.register(Product, ProductAdmin)
    admin.site.register(ProductCategory, ProductCategoryAdmin)
