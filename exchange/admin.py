
from django.contrib import admin

from solo.admin import SingletonModelAdmin

from exchange.models import ExchangeRates
from exchange.tasks import update_all_prices


@admin.register(ExchangeRates)
class ExchangeRatesAdmin(SingletonModelAdmin):

    list_display = ['id', 'usd', 'eur']
    list_editable = ['usd', 'eur']

    def save_model(self, *args):
        super().save_model(*args)
        update_all_prices()
