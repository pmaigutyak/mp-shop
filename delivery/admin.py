
from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from delivery.models import DeliveryMethod


@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(TranslationAdmin):

    list_display = ['name', 'code']
