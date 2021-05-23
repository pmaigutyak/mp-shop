
from django import forms
from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from attributes.fields import AttributesFormField
from product_images.fields import ImagesFormField
from availability.fields import AvailabilityField
from categories.fields import CategoryChoiceField
from cap.widgets import TagsInput, Select, SelectMultiple
from basement.forms import BasementModelForm

from cargo import constants


class ProductForm(BasementModelForm):

    # images = ImagesFormField()
    # attributes = AttributesFormField(label='')

    class Meta:
        # field_classes = {
        #     'availability': AvailabilityField,
        #     'category': CategoryChoiceField
        # }
        # widgets = {
        #     'tags': TagsInput,
        #     'additional_codes': TagsInput,
        #     'description': CKEditorUploadingWidget,
        #     'manufacturer': Select(select2attrs={'width': '100%'}),
        #     'category': Select(select2attrs={'width': '100%'}),
        #     'cars': SelectMultiple(select2attrs={
        #         'width': 'calc(100% - 20px)'
        #     })
        # }
        model = apps.get_model('products', 'Product')
        fields = '__all__'


class SearchProductForm(forms.Form):

    query = forms.CharField(label=_('Search query'), required=False)

    order_by = forms.ChoiceField(
        label=_('Order by'), choices=constants.PRODUCT_ORDER_CHOICES)

    price_from = forms.FloatField(required=False)

    price_to = forms.FloatField(required=False)

    page = forms.IntegerField()

    def set_filters(self, min_price=None, max_price=None):

        fields = self.fields

        fields['price_from'].widget.attrs['min'] = min_price
        fields['price_from'].widget.attrs['max'] = max_price
        fields['price_to'].widget.attrs['min'] = min_price
        fields['price_to'].widget.attrs['max'] = max_price
