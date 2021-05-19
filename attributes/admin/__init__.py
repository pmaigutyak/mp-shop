
from importlib import import_module

from django.apps import apps
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ordered_model.admin import OrderedModelAdmin

from attributes.admin.forms import AttributeForm, AttributeOptionInline
from attributes.models import Attribute


def _get_attribute_admin_base_class():

    if apps.is_installed('modeltranslation'):
        return import_module('modeltranslation.admin').TranslationAdmin

    return admin.ModelAdmin


@admin.register(Attribute)
class AttributeAdmin(OrderedModelAdmin, _get_attribute_admin_base_class()):

    form = AttributeForm
    inlines = [AttributeOptionInline]

    list_display = [
        'name', 'get_category_list', 'slug', 'get_type', 'is_required',
        'is_visible', 'is_filter', 'move_up_down_links']
    search_fields = ['name', 'slug']
    list_filter = ['categories', 'type', 'is_required']
    filter_horizontal = ['categories']
    fields = [
        'categories',
        'name',
        ('is_required', 'is_visible', 'is_filter', ),
        ('type', 'slug', ),
    ]

    def get_category_list(self, item):
        return ', '.join([c.name for c in item.categories.all()])

    get_category_list.short_description = _('Categories')

    def get_type(self, item):
        return item.get_type_display()

    get_type.short_description = _('Type')
