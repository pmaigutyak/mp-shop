
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


class ProductFlag(models.Model):

    title = models.CharField(_('Title'), max_length=255, blank=True)

    def __unicode__(self):
        return self.title

    def get_random_products(self, count=6):
        return self.products.visible().order_by('?')[:count]

    def get_absolute_url(self):
        return reverse('products:by-flag', kwargs={'flag_pk': self.pk})

    class Meta:
        verbose_name = _('Product flag')
        verbose_name_plural = _('Product flags')
