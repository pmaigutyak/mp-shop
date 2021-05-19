
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AttributeOption(models.Model):

    attr = models.ForeignKey(
        'attributes.Attribute',
        related_name='options',
        verbose_name=_("Attribute"),
        on_delete=models.CASCADE)

    name = models.CharField(_('Name'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('attr', 'name')
        verbose_name = _('Attribute option')
        verbose_name_plural = _('Attribute options')
