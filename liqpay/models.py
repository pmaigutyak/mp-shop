
import base64
import hashlib
import json

from urllib.parse import urljoin
from basement.services import register_service

from liqpay import config
from liqpay.forms import ApiForm, CheckoutForm
from liqpay.exceptions import LiqPayValidationError


def to_str(s):
    """
    :param s:
    :return: str value (decoded utf-8)
    """
    if isinstance(s, str):
        return s

    if hasattr(s, '__str__'):
        return s.__str__()

    return str(bytes(s), 'utf-8', 'strict')


class LiqPay(object):

    host = 'https://www.liqpay.ua/api/'

    checkout_url = urljoin(host, '3/checkout/')

    @staticmethod
    @register_service('liqpay')
    def _build(services, **kwargs):
        return LiqPay(
            public_key=config.LIQPAY_PUBLIC_KEY,
            private_key=config.LIQPAY_PRIVATE_KEY
        )

    def __init__(self, public_key, private_key):
        self._public_key = public_key
        self._private_key = private_key

    def get_checkout_form(self, **kwargs):

        params = self._clean_api_params(**kwargs)

        encoded_data = self.data_to_sign(params)

        return CheckoutForm(self.checkout_url, data={
            'data': encoded_data,
            'signature': self._make_signature(encoded_data)
        })

    def str_to_sign(self, str):
        return base64.b64encode(hashlib.sha1(str).digest())

    def data_to_sign(self, params):
        return base64.b64encode(json.dumps(params).encode("utf-8")).decode(
            "ascii")

    def _clean_api_params(self, **kwargs):

        params = {
            'version': 3,
            'currency': config.LIQPAY_DEFAULT_CURRENCY,
            'language': config.LIQPAY_DEFAULT_LANGUAGE,
            'action': config.LIQPAY_DEFAULT_ACTION,
            'public_key': self._public_key
        }

        params.update(kwargs)

        form = ApiForm(data=params)

        if not form.is_valid():
            raise LiqPayValidationError(
                'Invalid params: %s' % ', '.join(form.errors.keys()))

        return form.cleaned_data

    def _make_signature(self, data):

        params = [self._private_key, data, self._private_key]

        joined_fields = "".join(x for x in params)
        joined_fields = joined_fields.encode("utf-8")
        return base64.b64encode(hashlib.sha1(joined_fields).digest()).decode(
            "ascii")
