
from django.utils.translation import ugettext_lazy as _


def refresh_product_logos(modeladmin, request, queryset):
    for product in queryset:
        product.save()

refresh_product_logos.short_description = _('Refresh product logos')
