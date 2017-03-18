
from django.apps import apps
from django import forms


class CheckoutForm(forms.ModelForm):

    class Meta:
        model = apps.get_model('orders', 'Order')
        fields = [
            'name', 'surname', 'payment_method', 'delivery_method',
            'post_office', 'mobile', 'email', 'comment'
        ]
