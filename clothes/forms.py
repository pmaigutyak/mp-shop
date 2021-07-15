
from django import forms

from clothes.models import ClothesSize
from clothes.constants import (
    MALE_CLOTHES_FIELDS,
    FEMALE_CLOTHES_FIELDS,
    SEX_MALE,
    SEX_FEMALE
)


class MaleSizeForm(forms.ModelForm):

    sex = SEX_MALE

    class Meta:
        model = ClothesSize
        fields = MALE_CLOTHES_FIELDS


class FemaleSizeForm(forms.ModelForm):

    sex = SEX_FEMALE

    class Meta:
        model = ClothesSize
        fields = FEMALE_CLOTHES_FIELDS
