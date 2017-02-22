
from django import template

from shop.currencies.settings import CURRENCY_SESSION_KEY
from shop.currencies.forms import CurrencyForm


register = template.Library()


@register.assignment_tag(takes_context=True)
def get_currency_form(context):
    currency = context.request.session.get(CURRENCY_SESSION_KEY)
    return CurrencyForm(initial={'currency': currency})
