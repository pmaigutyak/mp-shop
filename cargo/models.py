
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from exchange.models import MultiCurrencyPrice
from exchange.constants import DEFAULT_CURRENCY_NAME

from availability.models import AvailabilityField
from manufacturers.models import ManufacturerField
from modeltranslation.utils import get_translation_fields
from categories.models import CategoryField
from clothes.constants import SEX_MALE, SEX_FEMALE, SEX_BOTH
from images.models import LogoField
from slugify import slugify_url

from cargo import model_fields
from cargo.managers import ProductManager


class AbstractProduct(MultiCurrencyPrice):

    is_visible = model_fields.IsVisibleField(_('Is visible on site'))

    category = CategoryField(related_name='products')

    manufacturer = ManufacturerField()

    availability = AvailabilityField()

    name = model_fields.NameField()

    code = model_fields.CodeField()

    description = model_fields.DescriptionField()

    logo = LogoField(upload_to='product_logos')

    created = model_fields.TimestampField()

    objects = ProductManager()

    @property
    def is_available(self):
        if self.availability:
            return self.availability.code == 'available'
        return False

    @property
    def manufacturer_name(self):
        if self.manufacturer:
            return self.manufacturer.name
        return ''

    @property
    def slug(self):
        if self.name:
            return slugify_url(self.name, separator='_')
        return 'product'

    @property
    def full_name(self):
        name = self.name

        if self.code:
            name += ' {}'.format(self.code)

        return name

    @property
    def printable_code(self):
        return self.code or _('Not specified')

    @property
    def printable_price(self):
        return '{} {}'.format(self.price_retail, DEFAULT_CURRENCY_NAME)

    def get_absolute_url(self):
        return reverse('products:product', args=[self.slug, self.id])

    @classmethod
    def get_translation_fields(cls):
        return ['name', 'description']

    @property
    def sex(self):
        try:
            return self.category.clothes_profile.sex
        except Exception:
            return ''

    def has_male_size(self):
        return self.sex in [SEX_MALE, SEX_BOTH]

    def has_female_size(self):
        return self.sex in [SEX_FEMALE, SEX_BOTH]

    @property
    def add_to_cart_attrs(self):
        attrs = [
            'data-role=add-to-cart',
            'data-product-id={}'.format(self.id)
        ]

        if self.sex:
            attrs.append('data-product-sex={}'.format(self.sex))

        return ' '.join(attrs)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        self._set_default_name_field()
        return super().save(**kwargs)

    def _set_default_name_field(self):

        fields = tuple(
            zip(
                get_translation_fields('name'),
                get_translation_fields('product_name')
            )
        ) + (('name', 'product_name',), )

        for src_field, dst_field in fields:

            if getattr(self, src_field):
                continue

            setattr(self, src_field, getattr(self.category, dst_field))

    class Meta:
        abstract = True
        ordering = ['-id']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


def get_product_manager(queryset_class):

    class Manager(ProductManager):

        def get_queryset(self):
            return queryset_class(self.model, using=self._db)

    return Manager()
