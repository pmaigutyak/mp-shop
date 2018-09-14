
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from slugify import slugify_url
from mptt.models import MPTTModel, TreeForeignKey
from shop.lib import get_file_upload_path, get_preview


def get_product_category_logo_upload_path(instance, filename):
    return get_file_upload_path('product_category_logos', filename)


class AbstractProductCategory(MPTTModel):

    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True)

    name = models.CharField(_('Name'), max_length=255, db_index=True)

    logo = models.ImageField(
        _("Logo"), upload_to=get_product_category_logo_upload_path,
        max_length=255, blank=True, null=True)

    description = models.TextField(_('Description'), blank=True)

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
        return get_preview(self.logo)

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
