
from django import forms

from clothes.models import ClothesSize
from clothes.constants import MALE_CLOTHES_FIELDS, FEMALE_CLOTHES_FIELDS


class MaleSizeForm(forms.ModelForm):

    class Meta:
        model = ClothesSize
        fields = MALE_CLOTHES_FIELDS


class FemaleSizeForm(forms.ModelForm):

    class Meta:
        model = ClothesSize
        fields = FEMALE_CLOTHES_FIELDS
