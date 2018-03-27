
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class EndangeredProductsFilter(admin.SimpleListFilter):

    title = _('Qty')
    parameter_name = 'is_endangered'

    def lookups(self, request, model_admin):
        return [('true', _('Endangered products'))]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(min_qty__gt=models.F('qty'))
        else:
            return queryset
