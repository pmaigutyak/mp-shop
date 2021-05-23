
from django.db import models
from django.utils.translation import ugettext_lazy as _

from basement.services import register_service

from clothes.constants import CLOTHES_FIELDS, SEX_CHOICES, SEX_MALE, SEX_FEMALE
from clothes.storage import SizeStorage


class SexField(models.CharField):

    def __init__(
            self,
            verbose_name=_('Sex'),
            max_length=10,
            choices=SEX_CHOICES,
            blank=True):
        super().__init__(
            verbose_name=verbose_name,
            max_length=max_length,
            choices=choices,
            blank=blank
        )


class CategoryProfile(models.Model):

    category = models.OneToOneField(
        'categories.Category',
        on_delete=models.CASCADE,
        verbose_name=_('Category'),
        related_name='clothes_profile'
    )

    grid = models.TextField(
        _('Size grid'),
        blank=True,
        max_length=4096)

    age = models.CharField(
        _('Age'),
        max_length=100,
        blank=True,
        choices=(
            ('adult', _('Adult')),
            ('child', _('Child'))
        )
    )

    sex = SexField()


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

    sex = SexField(blank=False)

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

        values = [
            (_('Sex'), self.get_sex_display()),
        ]

        for f_name in CLOTHES_FIELDS[self.sex]:

            value = getattr(self, f_name)

            if value:
                values.append((
                    self._meta.get_field(f_name).verbose_name, value
                ), )
        return values


class ClothesService(object):

    @staticmethod
    @register_service('clothes')
    def factory(services, user, session, **kwargs):
        return ClothesService(session)

    def __init__(self, session):
        self._storage = SizeStorage(session)

    def create_size(self, ordered_product):
        size = self._storage.get(ordered_product.product_id)

        male_values = size.get('male_form')

        if male_values:
            ClothesSize.objects.create(
                ordered_product=ordered_product,
                sex=SEX_MALE,
                **male_values)

        female_values = size.get('female_form')

        if female_values:
            ClothesSize.objects.create(
                ordered_product=ordered_product,
                sex=SEX_FEMALE,
                **female_values)
