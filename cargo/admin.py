
from django.utils.translation import ugettext_lazy as _

from modeltranslation.admin import TranslationAdmin

from cap.decorators import short_description, template_list_item
from cargo.forms import ProductForm
from images.actions import refresh_logos
from categories.actions import category_change_action


class CargoAdmin(TranslationAdmin):

    form = ProductForm

    actions = [
        category_change_action,
        refresh_logos
    ]

    list_display_links = ['id', 'name']

    list_filter = ['category', 'availability']

    ordering = ['-id']

    @short_description(_('Price'))
    def printable_price(self, item):
        return item.printable_price

    @template_list_item('admin/list_item_preview.html', _('Preview'))
    def get_preview(self, item):
        return {'file': item.logo}

    @template_list_item('products/admin/list_item_actions.html', _('Actions'))
    def get_item_actions(self, item):
        return {'object': item}

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        form.commit(obj)
