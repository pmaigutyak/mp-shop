
from django.db import models

from exchange.querysets import MultiCurrencyQuerySet


class MultiCurrencyManager(models.Manager):

    def get_queryset(self):
        return MultiCurrencyQuerySet(self.model, using=self._db)

    def set_currency(self, value):
        return self.get_queryset().set_currency(value)
