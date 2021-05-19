
from django import forms
from django.utils.translation import ugettext_lazy as _

from delivery.models import DeliveryMethod


class DeliveryForm(forms.Form):

    delivery_method = forms.ModelChoiceField(
        label=_('Delivery method'),
        queryset=DeliveryMethod.objects.all())

    city = forms.CharField(
        label=_('City'),
        required=False
    )

    warehouse = forms.CharField(
        label=_('Warehouse'),
        required=False
    )

    @property
    def delivery_methods(self):
        return {m.code: m.id for m in DeliveryMethod.objects.all()}
