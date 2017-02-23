
from django import forms


class CartItemForm(forms.Form):

    qty = forms.IntegerField(min_value=1, max_value=100000, initial=1)
