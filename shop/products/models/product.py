
from random import randint

from django.core.files import File
from django.core.urlresolvers import reverse
from django.apps import apps
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from slugify import slugify_url

from shop.currencies.lib import format_printable_price
from shop.currencies.models import ExchangeRate
from shop.currencies.settings import CURRENCIES, DEFAULT_CURRENCY
from shop.lib import get_preview


class ProductQuerySet(models.QuerySet):

    def visible(self):
        return self.filter(is_visible=True)


class ProductManager(models.Manager):

    def get_query_set(self):
        return ProductQuerySet(self.model, using=self._db)

    def visible(self):
        return self.filter(is_visible=True)


class ProductVisibilityManager(models.Manager):

    def get_queryset(self):
        queryset = super(ProductVisibilityManager, self).get_queryset()
        return queryset.filter(is_visible=True)


class Price(object):

    def __init__(self, obj):
        self.obj = obj

    @property
    def currency(self):
        return self.obj.currency

    def printable_currency(self):
        return self.obj.get_currency_display()

    @property
    def default(self):
        return ExchangeRate.convert(
            price=self.obj.price_in_currency,
            src_currency=self.obj.currency,
            dst_currency=DEFAULT_CURRENCY)

    @property
    def printable_default(self):
        return ExchangeRate.convert(
            price=self.obj.price_in_currency,
            src_currency=self.obj.currency,
            dst_currency=DEFAULT_CURRENCY,
            printable=True)

    @property
    def initial(self):
        return self.obj.price_in_currency

    @property
    def printable_initial(self):
        return format_printable_price(self.initial, self.currency)


class AbstractProduct(models.Model):

    is_visible = models.BooleanField(_('Is visible'), default=True)

    category = models.ForeignKey(
        'products.ProductCategory', verbose_name=_("Category"),
        related_name='products', blank=False)

    title = models.CharField(_('Title'), max_length=255, blank=True)

    code = models.CharField(_('Code'), max_length=255, blank=True)

    price_in_currency = models.FloatField(_('Price'), blank=False, null=False)

    currency = models.PositiveSmallIntegerField(
        _('Currency'), choices=CURRENCIES, default=DEFAULT_CURRENCY)

    description = models.TextField(_('Description'), blank=True)

    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)

    date_updated = models.DateTimeField(
        _("Date updated"), auto_now=True, db_index=True)

    logo = models.ImageField(
        _("Logo"), upload_to='product_logos', max_length=255,
        blank=True, null=True, editable=False)

    objects = ProductManager()
    visible = ProductVisibilityManager()

    def __init__(self, *args, **kwargs):

        super(AbstractProduct, self).__init__(*args, **kwargs)

        self.price = Price(self)

    def refresh_logo(self):

        first_image = self.images.first()

        if first_image:
            file = File(open(first_image.file.path))
            self.logo.save(first_image.file.name, file)
        else:
            self.logo.delete()

    @property
    def slug(self):
        return slugify_url(self.title, separator='_')

    @property
    def printable_code(self):
        return self.code or _('Not specified')

    @property
    def preview(self):
        return get_preview(self.logo)

    preview.fget.short_description = _('Preview')

    @classmethod
    def get_related_products(cls, category, exclude_pk, count=6):

        index = 0

        related_products = cls.objects.filter(
            is_visible=True, category=category).exclude(pk=exclude_pk)

        related_products_count = len(related_products)

        if related_products_count:

            if related_products_count > count:
                index = randint(0, related_products_count - count)

            return related_products[index:index + count]

        return []

    @property
    def related_products(self):
        if not hasattr(self, '_related_products'):
            self._related_products = self.get_related_products(
                self.category, self.pk)

        return self._related_products

    @classmethod
    def get_search_fields(cls):

        if not apps.is_installed('modeltranslation'):
            return ['code', 'title', 'description']

        fields = ['code']

        for language in dict(settings.LANGUAGES).keys():
            fields.append('title_%s' % language)
            fields.append('description_%s' % language)

        return fields

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:info', kwargs={
            'product_slug': self.slug, 'product_pk': self.id})

    class Meta:
        abstract = True
        ordering = ['-id']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
