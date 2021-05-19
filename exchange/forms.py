
from django import forms

from exchange.constants import CURRENCIES


class CurrencyForm(forms.Form):
    currency = forms.ChoiceField(choices=CURRENCIES, required=True)
