
from django.apps import apps
from django import forms
from django.utils.translation import ugettext_lazy as _

from suit.sortables import SortableTabularInline
from multiupload.fields import MultiFileField


class ProductForm(forms.ModelForm):

    images = MultiFileField(
        label=_('Images'), max_num=100, min_num=1, required=False)

    class Meta:
        model = apps.get_model('products', 'Product')
        fields = '__all__'


class ProductImageInline(SortableTabularInline):
    fields = ('preview', )
    readonly_fields = ['preview']
    model = apps.get_model('products', 'ProductImage')
    extra = 0
    max_num = 0

