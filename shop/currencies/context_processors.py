
from shop.currencies.settings import CURRENCIES, CURRENCY_SESSION_KEY


def defaults(request):
    return {
        'CURRENCIES': CURRENCIES,
        'CURRENCY': request.session.get(CURRENCY_SESSION_KEY)
    }
