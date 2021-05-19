
from django.apps import apps
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mptt.admin import MPTTModelAdmin
from modeltranslation.admin import TranslationAdmin
from modeltranslation.utils import get_translation_fields
from cap.decorators import short_description, template_list_item

from categories.models import Category
from categories.config import IS_CLOTHES_BUSINESS


def _get_formfield_overrides():

    if apps.is_installed('ckeditor'):
        from ckeditor.widgets import CKEditorWidget
        return {
            models.TextField: {'widget': CKEditorWidget}
        }

    return {}


def _get_list_display():
    result = (
        ['id'] +
        get_translation_fields('name') +
        get_translation_fields('title')
    )

    if IS_CLOTHES_BUSINESS:
        result += ['age']

    return result + ['code', 'icon', 'product_count', 'get_preview']


@admin.register(Category)
class CategoryAdmin(TranslationAdmin, MPTTModelAdmin):

    list_editable = (
        get_translation_fields('title') +
        get_translation_fields('name')
    )

    fields = (
        ('parent', 'code', ),
        tuple(get_translation_fields('name')),
        tuple(get_translation_fields('title')),
        ('logo', 'icon', ),
        tuple(get_translation_fields('description')),
    )

    list_display = _get_list_display()

    formfield_overrides = _get_formfield_overrides()

    @property
    def fields(self):
        fields = (
            ('parent', 'code',),
            tuple(get_translation_fields('name')),
            tuple(get_translation_fields('title')),

        )

        if IS_CLOTHES_BUSINESS:
            fields += (
                ('age', 'grid',),
            )

        return fields + (
            ('logo', 'icon',),
            tuple(get_translation_fields('description')),
        )

    @template_list_item('admin/list_item_preview.html', _('Preview'))
    def get_preview(self, item):
        return {'file': item.logo}

    @short_description(_('Product count'))
    def product_count(self, item):
        return item.products.count()
