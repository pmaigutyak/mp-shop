
from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from labels.models import ProductLabel


admin.site.register(ProductLabel, TranslationAdmin)
