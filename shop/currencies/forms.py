
from django import forms

from shop.currencies.settings import CURRENCIES


class CurrencyForm(forms.Form):
    currency = forms.ChoiceField(choices=CURRENCIES, required=True)
