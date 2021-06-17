
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class ProductLabel(models.Model):

    title = models.CharField(_('Title'), max_length=255, blank=True)

    def __str__(self):
        return self.title

    def get_random_products(self, count=6):
        return self.products.visible().order_by('?')[:count]

    def get_absolute_url(self):
        return reverse('labels:products', kwargs={'label_id': self.id})

    class Meta:
        verbose_name = _('Product label')
        verbose_name_plural = _('Product labels')


class LabelsField(models.ManyToManyField):

    def __init__(
            self,
            to=ProductLabel,
            verbose_name=_('Labels'),
            related_name='products',
            blank=True,
            *args, **kwargs):

        super(LabelsField, self).__init__(
            to,
            verbose_name=verbose_name,
            related_name=related_name,
            blank=blank,
            *args, **kwargs)
