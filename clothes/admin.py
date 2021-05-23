
from django.apps import apps
from django.db import models
from django.contrib import admin

from modeltranslation.admin import TranslationAdmin
from modeltranslation.utils import get_translation_fields

from clothes.models import CategoryProfile


def _get_formfield_overrides():

    if apps.is_installed('ckeditor'):
        from ckeditor.widgets import CKEditorWidget
        return {
            models.TextField: {'widget': CKEditorWidget}
        }

    return {}


@admin.register(CategoryProfile)
class CategoryProfileAdmin(TranslationAdmin):

    list_editable = ('age', 'sex', )

    list_display = ('id', 'category', 'age', 'sex', )

    formfield_overrides = _get_formfield_overrides()

    fields = (
        'category',
        ('age', 'sex', ),
        tuple(get_translation_fields('grid')),
    )
