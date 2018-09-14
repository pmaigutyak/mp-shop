
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AbstractProductTag(models.Model):

    text = models.CharField(_('Text'), max_length=255, unique=True)

    def __unicode__(self):
        return self.text

    class Meta:
        abstract = True
        verbose_name = _('Product tag')
        verbose_name_plural = _('Products tags')
