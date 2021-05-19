
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from exchange.models import MultiCurrencyPrice
from availability.models import AvailabilityField
from manufacturers.models import ManufacturerField
from categories.models import CategoryField
from basement.images.models import LogoField
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

    def get_absolute_url(self):
        return reverse('products:product', kwargs={
            'product_slug': self.slug,
            'product_id': self.id
        })

    @classmethod
    def get_translation_fields(cls):
        return ['name', 'description']

    def __str__(self):
        return self.name

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
