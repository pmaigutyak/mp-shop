
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

from slugify import slugify_url


class Category(MPTTModel):

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('Parent category'))

    name = models.CharField(
        _('Category name'),
        max_length=255)

    title = models.CharField(
        _('Category title'),
        max_length=255,
        blank=True)

    product_name = models.CharField(
        _('Product name'),
        max_length=255,
        blank=True)

    logo = models.ImageField(
        _('Logo'),
        upload_to='categories',
        blank=True,
        null=True,
        max_length=255)

    code = models.CharField(
        _('Code'),
        max_length=255,
        blank=True)

    icon = models.CharField(
        _('Icon'),
        max_length=255,
        blank=True)

    description = models.TextField(
        _('Description'),
        blank=True,
        max_length=4096)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('products:list', args=[self.slug, self.id])

    @property
    def slug(self):
        return slugify_url(self.name or 'category', separator='_')

    @property
    def full_name(self):
        return ' > '.join([
            c.name for c in self.get_ancestors(include_self=True)
        ])

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class CategoryField(models.ForeignKey):

    def __init__(
            self,
            to='categories.Category',
            verbose_name=_('Category'),
            on_delete=models.CASCADE,
            *args, **kwargs):

        super(CategoryField, self).__init__(
            to,
            verbose_name=verbose_name,
            on_delete=on_delete,
            *args, **kwargs)
