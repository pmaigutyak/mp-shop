
from random import randint

from django.apps import apps
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils import timezone

from sorl.thumbnail import get_thumbnail
from slugify import slugify_url
from mptt.models import MPTTModel, TreeForeignKey
from ordered_model.models import OrderedModelBase

from shop.currencies.lib import format_printable_price
from shop.currencies.models import ExchangeRate
from shop.currencies.settings import CURRENCIES, DEFAULT_CURRENCY


def get_file_upload_path(folder, filename):
    tz_now = timezone.localtime(timezone.now()).strftime('%Y_%m_%d_%H_%M')
    return '%s/%s.%s' % (folder, tz_now, filename.split('.')[-1])


def get_product_image_upload_path(instance, filename):
    return get_file_upload_path('product_images', filename)


def get_product_category_logo_upload_path(instance, filename):
    return get_file_upload_path('product_category_logos', filename)


class AbstractProductCategory(MPTTModel):

    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True)

    name = models.CharField(_('Name'), max_length=255, db_index=True)

    logo = models.ImageField(
        _("Logo"), upload_to=get_product_category_logo_upload_path,
        max_length=255, blank=True, null=True)

    _slug_separator = '/'
    _full_name_separator = ' > '

    @property
    def slug(self):
        return slugify_url(self.name, separator='_')

    @property
    def ancestors(self):
        return self.get_ancestors(include_self=True)

    @property
    def full_slug(self):
        slugs = [category.slug for category in self.ancestors]
        return self._slug_separator.join(slugs)

    @property
    def full_name(self):
        try:
            names = [category.name for category in self.ancestors]
            return self._full_name_separator.join(names)
        except ValueError:
            return self.name

    full_name.fget.short_description = _('Full name')

    @property
    def preview(self):
        try:
            url = get_thumbnail(
                self.logo.file, '100x100', crop='center', quality=99).url
        except Exception:
            return '-----'

        return mark_safe('<img src="%s" style="width: 100px;" />' % url)

    preview.fget.short_description = _('Preview')

    def __unicode__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('products:category', kwargs={
            'category_slug': self.full_slug, 'category_pk': self.pk})

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        abstract = True
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


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
        _("Logo"), upload_to=get_product_image_upload_path, max_length=255,
        blank=True, null=True, editable=False)

    objects = ProductManager()
    visible = ProductVisibilityManager()

    def __init__(self, *args, **kwargs):

        self._saved = False

        super(AbstractProduct, self).__init__(*args, **kwargs)

        self.price = ProductPriceContainer(self)

    def save(self, *args, **kwargs):
        super(AbstractProduct, self).save(*args, **kwargs)

        if not self._saved:
            self._saved = True
            photo = self.images.first()
            if photo:
                self.logo.name = photo.file.path
                self.save(update_fields=['logo'])

    @property
    def slug(self):
        return slugify_url(self.title, separator='_')

    @property
    def printable_code(self):
        return self.code or _('Not specified')

    @property
    def preview(self):
        try:
            url = get_thumbnail(
                self.logo.file, '100x100', crop='center', quality=99).url
        except Exception:
            return '-----'

        return mark_safe('<img src="%s" style="width: 100px;" />' % url)

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


class ProductPriceContainer(object):

    def __init__(self, product):
        self.product = product

    @property
    def currency(self):
        return self.product.currency

    def printable_currency(self):
        return self.product.get_currency_display()

    @property
    def default(self):
        return ExchangeRate.convert(
            price=self.product.price_in_currency,
            src_currency=self.product.currency,
            dst_currency=DEFAULT_CURRENCY)

    @property
    def printable_default(self):
        return ExchangeRate.convert(
            price=self.product.price_in_currency,
            src_currency=self.product.currency,
            dst_currency=DEFAULT_CURRENCY,
            printable=True)

    @property
    def initial(self):
        return self.product.price_in_currency

    @property
    def printable_initial(self):
        return format_printable_price(self.initial, self.currency)


class AbstractProductImage(OrderedModelBase):

    product = models.ForeignKey(
        'products.Product', related_name='images', verbose_name=_("Product"))

    file = models.ImageField(
        _("File"), upload_to=get_product_image_upload_path, max_length=255)

    order = models.PositiveIntegerField(_('Ordering'), default=0)

    order_field_name = 'order'
    order_with_respect_to = 'product'

    def __unicode__(self):
        return self.product.title

    @property
    def preview(self):
        try:
            url = get_thumbnail(
                self.file.file, '100x100', crop='center', quality=99).url
        except Exception:
            return '-----'

        return mark_safe('<img src="%s" style="width: 100px;" />' % url)

    preview.fget.short_description = _('Preview')

    class Meta:
        abstract = True
        ordering = ('order', 'id', )
        verbose_name = _('Product image')
        verbose_name_plural = _('Product images')
