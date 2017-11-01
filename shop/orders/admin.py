
from django.apps import apps
from django.conf import settings
from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from shop.lib import get_show_on_site_link


class OrderProductInline(admin.TabularInline):

    model = apps.get_model('orders', 'OrderProduct')
    extra = 0


class OrderProductForm(forms.ModelForm):

    def clean_title(self):
        data = self.cleaned_data

        title = data.get('title')
        parent = data.get('parent')

        if parent and not title:
            title = parent.title

        if not parent and not title:
            raise forms.ValidationError(_('Select product or enter title'))

        return title

    def clean_price(self):
        data = self.cleaned_data

        price = data.get('price')
        parent = data.get('parent')

        if parent and not price:
            price = parent.price

        if not parent and not price:
            raise forms.ValidationError(_('Select product or enter price'))

        return price

    class Meta:
        model = apps.get_model('orders', 'OrderProduct')
        fields = '__all__'


class OrderAdmin(admin.ModelAdmin):

    inlines = [OrderProductInline]

    list_display = [
        'printable_name', 'name', 'mobile', 'post_office', 'email',
        'date_created', 'product_count', 'printable_default_total', 'status',
        'get_preview'
    ]

    search_fields = ['id', 'name', 'mobile', 'post_office', 'email']

    list_editable = ['status']

    def get_preview(self, item):

        try:
            return item.products.first().parent.preview
        except Exception:
            return '----'

    get_preview.short_description = _('Preview')


class OrderProductAdmin(admin.ModelAdmin):

    form = OrderProductForm

    list_display = [
        'product_title', 'price', 'qty', 'order_name', 'get_show_link',
        'get_preview'
    ]

    search_fields = ['title', 'price', 'parent__code', 'parent__title']

    list_filter = ['order']

    def get_show_link(self, item):

        if item.parent:
            return get_show_on_site_link(item.parent.get_absolute_url())

        return '----'

    get_show_link.short_description = _('Show on site')

    def get_preview(self, item):

        if item.parent:
            return item.parent.preview

        return '----'

    get_preview.short_description = _('Preview')


if 'shop.orders' in settings.INSTALLED_APPS:

    from shop.orders.models import Order, OrderProduct

    admin.site.register(Order, OrderAdmin)
    admin.site.register(OrderProduct, OrderProductAdmin)
