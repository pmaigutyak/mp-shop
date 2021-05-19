
from django import template

from exchange.utils import get_currency_from_session
from exchange.forms import CurrencyForm


register = template.Library()


@register.simple_tag(takes_context=True)
def get_currency_form(context):
    currency = get_currency_from_session(context.request.session)
    return CurrencyForm(initial={'currency': currency})
