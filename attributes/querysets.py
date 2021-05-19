
from django.db.models import QuerySet


class AttributeValueQuerySet(QuerySet):

    def visible(self):
        return self.filter(attr__is_visible=True)
