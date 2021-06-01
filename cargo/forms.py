
from django import forms
from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from attributes.fields import AttributesFormField
from product_images.fields import ImagesFormField
from basement.forms import BasementModelForm

from cargo import constants


class ProductForm(BasementModelForm):

    images = ImagesFormField()
    attributes = AttributesFormField(label='')

    class Meta:
        model = apps.get_model('products', 'Product')
        fields = '__all__'


class ProductFilterForm(forms.Form):

    query = forms.CharField(
        label=_('Search query'),
        required=False)

    order_by = forms.ChoiceField(
        label=_('Order by'),
        choices=constants.PRODUCT_ORDER_CHOICES,
        required=False)

    price_from = forms.FloatField(required=False)

    price_to = forms.FloatField(required=False)

    def set_filters(self, min_price=None, max_price=None):

        fields = self.fields

        fields['price_from'].widget.attrs['min'] = min_price
        fields['price_from'].widget.attrs['max'] = max_price
        fields['price_to'].widget.attrs['min'] = min_price
        fields['price_to'].widget.attrs['max'] = max_price
