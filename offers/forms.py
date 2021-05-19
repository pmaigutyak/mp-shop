
from django import forms

from captcha.fields import ReCaptchaField

from offers.models import ProductPriceOffer


class ProductPriceOfferForm(forms.ModelForm):

    captcha = ReCaptchaField()

    class Meta:
        model = ProductPriceOffer
        fields = ('name', 'mobile', 'email', 'text', )
