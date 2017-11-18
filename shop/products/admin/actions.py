
from django.utils.translation import ugettext_lazy as _

from shop.products import lib


def refresh_products_logos(modeladmin, request, queryset):
    lib.refresh_products_logos(list(queryset.values_list('id', flat=True)))

refresh_products_logos.short_description = _('Refresh product logos')
