
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ProductAttrOption(models.Model):

    attr = models.ForeignKey(
        'products.ProductAttr', related_name='options',
        verbose_name=_("Attribute"))

    name = models.CharField(_('Name'), max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('attr', 'name')
        verbose_name = _('Attribute option')
        verbose_name_plural = _('Attribute options')
