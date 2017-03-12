
from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from shop.flags.models import ProductFlag


class ProductFlagAdmin(TranslationAdmin):
    pass


admin.site.register(ProductFlag, ProductFlagAdmin)
