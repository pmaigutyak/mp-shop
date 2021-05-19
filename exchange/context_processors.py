
from exchange.utils import get_currency_from_session
from exchange.constants import CURRENCIES


def currencies(request):
    return {
        'CURRENCY': get_currency_from_session(request.session),
        'CURRENCIES': CURRENCIES
    }
