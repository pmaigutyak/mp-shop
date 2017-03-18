
from django.apps import apps

from django import forms

from suit.sortables import SortableTabularInline
from multiupload.fields import MultiFileField


class ProductForm(forms.ModelForm):

    images = MultiFileField(max_num=100, min_num=1, required=False)

    # def __init__(self, *args, **kwargs):
    #
    #     super(ProductForm, self).__init__(*args, **kwargs)
    #
    #     if self.instance.pk is not None:
    #         self.fields.pop('category')

    class Meta:
        model = apps.get_model('products', 'Product')
        fields = '__all__'


class ProductImageInline(SortableTabularInline):
    fields = ('preview', )
    readonly_fields = ['preview']
    model = apps.get_model('products', 'ProductImage')
    extra = 0
    max_num = 0

