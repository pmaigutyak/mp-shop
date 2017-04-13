
from django.apps import apps

from django import forms

from suit.sortables import SortableTabularInline
from multiupload.fields import MultiFileField


class ProductForm(forms.ModelForm):

    images = MultiFileField(max_num=100, min_num=1, required=False)

    def save(self, commit=True):
        product = super(ProductForm, self).save()

        if 'category' in self.changed_data:
            product.attribute_values.all().delete()

        images = self.cleaned_data.get('images', [])

        for image in images:
            if image:
                product.images.create(file=image)

        return product

    class Meta:
        model = apps.get_model('products', 'Product')
        fields = '__all__'


class ProductImageInline(SortableTabularInline):
    fields = ('preview', )
    readonly_fields = ['preview']
    model = apps.get_model('products', 'ProductImage')
    extra = 0
    max_num = 0

