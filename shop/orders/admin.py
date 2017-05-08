
from django.apps import apps
from django.conf import settings
from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


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

    list_display = (
        'printable_name', 'name', 'mobile', 'post_office', 'email',
        'date_created', 'product_count', 'printable_default_total', 'status',
    )

    search_fields = ('id', 'name', 'mobile', 'post_office', 'email', )

    list_editable = ['status']


class OrderProductAdmin(admin.ModelAdmin):

    form = OrderProductForm

    list_display = (
        'product_title', 'price', 'qty', 'order_name', 'show_on_site', )

    search_fields = ['title', 'price', 'parent__code', 'parent__title']

    list_filter = ('order', )

    def show_on_site(self, item):
        if not item.parent:
            return '----'

        label = _('Show on site')

        template = '<a href="%s" target="_blank">%s</a>'

        return template % (item.parent.get_absolute_url(), label)

    show_on_site.short_description = _('Show on site')
    show_on_site.allow_tags = True


if 'shop.orders' in settings.INSTALLED_APPS:

    from shop.orders.models import Order, OrderProduct

    admin.site.register(Order, OrderAdmin)
    admin.site.register(OrderProduct, OrderProductAdmin)
