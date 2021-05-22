
from django.db import models
from django.utils.translation import ugettext_lazy as _

from clothes.constants import CLOTHES_FIELDS


class ClothesSize(models.Model):

    MALE_SIZES = (
        (44, '44 (S)'),
        (46, '46 (M)'),
        (48, '48 (M)'),
        (50, '50 (L)'),
        (52, '52 (XL)'),
        (54, '54 (XXL)'),
        (56, '56 (XXL)'),
        (58, '58 (XXL)'),
        (60, '60 (XXXL)'),
        (62, '62 (XXXL)'),
    )

    FEMALE_SIZES = (
        (42, '42 (S)'),
        (44, '44 (M)'),
        (46, '46 (M)'),
        (48, '48 (L)'),
        (50, '50 (XL)'),
        (52, '52 (XXL)'),
        (54, '54 (XXL)'),
        (56, '56 (XXL)'),
        (58, '58 (XXXL)'),
        (60, '60 (XXXL)'),
    )

    SIZE_CHOICES = MALE_SIZES + FEMALE_SIZES

    size = models.IntegerField(
        _('Size'),
        choices=SIZE_CHOICES)

    ordered_product = models.ForeignKey(
        'orders.OrderedProduct',
        verbose_name=_('Ordered product'),
        related_name='clothe_sizes',
        on_delete=models.CASCADE)

    breast_size = models.IntegerField(
        _('Breast size'),
        blank=True,
        null=True)

    waist_volume = models.IntegerField(
        _('Waist volume'),
        blank=True,
        null=True)

    hips_volume = models.IntegerField(
        _('Hips volume'),
        blank=True,
        null=True)

    sleeve_length = models.IntegerField(
        _('Length of the sleeve from the shoulder'),
        blank=True,
        null=True)

    shoulder_length = models.IntegerField(
        _('Shoulder length'),
        blank=True,
        null=True)

    product_length = models.IntegerField(
        _('Product length'),
        blank=True,
        null=True)

    back_width = models.IntegerField(
        _('Back width'),
        blank=True,
        null=True)

    neck_volume = models.IntegerField(
        _('Neck volume'),
        blank=True,
        null=True)

    length_of_dress_up_to_waist = models.IntegerField(
        _('Length of dress up to waist'), blank=True, null=True)

    length_of_dress_from_waist = models.IntegerField(
        _('Length of dress from waist'), blank=True, null=True)

    def get_values(self):
        values = []
        for f_name in CLOTHES_FIELDS:
            values.append((
                self._meta.get_field(f_name).verbose_name,
                getattr(self, f_name)
            ), )
        return values
