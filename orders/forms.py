
from django import forms

from orders.models import Order, ClothesSize
from orders.constants import MALE_CLOTHES_FIELDS, FEMALE_CLOTHES_FIELDS

from delivery.fields import DeliveryFormField


class CheckoutForm(forms.ModelForm):

    delivery = DeliveryFormField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['delivery'].init_form(*args, **kwargs)

    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'middle_name', 'payment_method',
            'mobile', 'comment'
        ]


class MaleSizeForm(forms.ModelForm):

    class Meta:
        model = ClothesSize
        fields = MALE_CLOTHES_FIELDS


class FemaleSizeForm(forms.ModelForm):

    class Meta:
        model = ClothesSize
        fields = FEMALE_CLOTHES_FIELDS
