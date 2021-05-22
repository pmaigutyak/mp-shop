
from exchange.utils import get_currency_from_session


class ExchangeService(object):

    def __init__(self, user, session):
        self._user = user
        self._session = session

    def get_active_currency(self):
        return get_currency_from_session(self._session)
