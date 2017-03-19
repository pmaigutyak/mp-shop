
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from modeltranslation.admin import TranslationAdmin

from shop.attributes.admin.forms import (
    ProductAttributeForm, AttributeOptionInline)
from shop.attributes.models import AttributeOptionGroup, ProductAttribute


class ProductAttributeAdmin(TranslationAdmin):

    form = ProductAttributeForm

    list_display = (
        'name', 'category', 'slug', 'get_type_display', 'required',
        'is_filter',
    )
    search_fields = ('name', 'slug', )
    list_filter = ('category', 'type', 'required', )


class AttributeOptionGroupAdmin(admin.ModelAdmin):

    inlines = [AttributeOptionInline]

    list_display = ('name', 'attribute', 'category', )
    search_fields = ('name', 'attribute__name', )
    list_filter = ('attribute__category', )

    def category(self, item):
        return item.attribute.category
    category.short_description = _('Category')


class ProductAdminMixin(object):

    def render_change_form(self, request, context, **kwargs):

        form = context['adminform'].form

        fieldsets = self.fieldsets or [(None, {'fields': form.fields.keys()})]

        context['adminform'] = admin.helpers.AdminForm(
            form, fieldsets, self.prepopulated_fields, model_admin=self)

        return super(ProductAdminMixin, self).render_change_form(
            request, context, **kwargs)


admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(AttributeOptionGroup, AttributeOptionGroupAdmin)