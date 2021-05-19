
from django.db.models import Manager

from attributes.querysets import AttributeValueQuerySet


class AttributeValueManager(Manager):

    def get_queryset(self):
        return AttributeValueQuerySet(self.model, using=self._db)

    def visible(self):
        return self.get_queryset().visible()
