
from django import forms

from shop.currencies.settings import CURRENCIES


class SetCurrencyForm(forms.Form):
    currency = forms.ChoiceField(choices=CURRENCIES, required=True)
