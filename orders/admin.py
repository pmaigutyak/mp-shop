
from django.apps import apps
from django.contrib import admin
from django.utils.timezone import localtime
from django.utils.translation import ugettext_lazy as _

from cap.decorators import template_list_item, short_description

from orders.constants import DAYS_OF_WEEK
from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = [
        'order_tag', 'customer_tag', 'delivery_tag', 'status', 'products_tag']

    list_editable = ['status']

    list_filter = ['status']

    search_fields = [
        'first_name', 'last_name', 'middle_name', 'address', 'mobile',
        'comment'
    ]

    def has_add_permission(self, request):
        return False

    @template_list_item('orders/admin/customer.html', _('Customer'))
    def customer_tag(self, obj):
        return {'object': obj}

    @template_list_item('orders/admin/delivery.html', _('Delivery'))
    def delivery_tag(self, obj):
        return {'object': obj}

    @template_list_item('orders/admin/products.html', _('Products'))
    def products_tag(self, obj):
        return {
            'object': obj,
            'is_clothes_app_enabled': apps.is_installed('clothes')
        }

    @short_description(_('Order'))
    def order_tag(self, obj):
        created = localtime(obj.created)
        day = DAYS_OF_WEEK[created.weekday()]
        return '#{} - ({}) {}'.format(
            obj.id, day, created.strftime('%d.%m.%Y %H:%M'))
