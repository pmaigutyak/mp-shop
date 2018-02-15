
from django.utils.translation import ugettext_lazy as _


def refresh_products_logos(modeladmin, request, queryset):
    for product in queryset:
        product.refresh_logo()

refresh_products_logos.short_description = _('Refresh product logos')
