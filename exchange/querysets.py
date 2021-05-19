
from django.db import models
from django.db.models import Value, IntegerField
from django.core.handlers.wsgi import WSGIRequest

from exchange.utils import get_currency_from_session


class MultiCurrencyQuerySet(models.QuerySet):

    def set_currency(self, value):

        if isinstance(value, WSGIRequest):
            currency = get_currency_from_session(value.session)
        else:
            currency = value

        return self.annotate(
            annotated_currency=Value(currency, IntegerField())
        )
