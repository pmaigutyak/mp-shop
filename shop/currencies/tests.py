
from django.test import TestCase
from django.test.utils import override_settings
from django.test.client import RequestFactory
from django.template import Template, RequestContext

from shop.currencies.models import ExchangeRate


CURRENCY_UAH = 1
CURRENCY_USD = 2
CURRENCY_EUR = 3


CURRENCIES = (
    (CURRENCY_UAH, 'UAH'),
    (CURRENCY_USD, 'USD'),
    (CURRENCY_EUR, 'EUR'),
)

USD_COURSE = 27.5
EUR_COURSE = 29

CURRENCY_SESSION_KEY = 'CURRENCY'


@override_settings(CURRENCIES=CURRENCIES, DEFAULT_CURRENCY=CURRENCY_UAH)
class ExchangeRateTest(TestCase):

    def setUp(self):
        ExchangeRate.objects.create(currency=CURRENCY_USD, value=USD_COURSE)
        ExchangeRate.objects.create(currency=CURRENCY_EUR, value=EUR_COURSE)

    def test_get_exchange_rates_returns_correct_data(self):

        exchange_rates = ExchangeRate.get_exchange_rates()

        self.assertEqual(exchange_rates[CURRENCY_UAH], 1)
        self.assertEqual(exchange_rates[CURRENCY_USD], 27.5)
        self.assertEqual(exchange_rates[CURRENCY_EUR], 29.0)

    def test_convert_from_uah_to_usd(self):

        self.assertEqual(
            ExchangeRate.convert(2750, CURRENCY_UAH, CURRENCY_USD), 100.0)

        self.assertEqual(
            ExchangeRate.convert(150, CURRENCY_UAH, CURRENCY_USD),
            5.454545454545454)

    def test_convert_from_uah_to_eur(self):

        self.assertEqual(
            ExchangeRate.convert(2900, CURRENCY_UAH, CURRENCY_EUR), 100.0)

        self.assertEqual(
            ExchangeRate.convert(100, CURRENCY_UAH, CURRENCY_EUR),
            3.4482758620689653)

    def test_convert_from_eur_to_uah(self):

        self.assertEqual(
            ExchangeRate.convert(100, CURRENCY_EUR, CURRENCY_UAH), 2900)

        self.assertEqual(
            ExchangeRate.convert(125, CURRENCY_EUR, CURRENCY_UAH), 3625.0)

    def test_convert_from_eur_to_usd(self):

        self.assertEqual(
            ExchangeRate.convert(100, CURRENCY_EUR, CURRENCY_USD),
            105.45454545454545)

        self.assertEqual(
            ExchangeRate.convert(125, CURRENCY_EUR, CURRENCY_USD),
            131.81818181818184)

    def test_convert_from_usd_to_uah(self):

        self.assertEqual(
            ExchangeRate.convert(100, CURRENCY_USD, CURRENCY_UAH), 2750)

        self.assertEqual(
            ExchangeRate.convert(125, CURRENCY_USD, CURRENCY_UAH), 3437.5)

    def test_convert_from_usd_to_eur(self):

        self.assertEqual(
            ExchangeRate.convert(100, CURRENCY_USD, CURRENCY_EUR),
            94.82758620689654)

        self.assertEqual(
            ExchangeRate.convert(125, CURRENCY_USD, CURRENCY_EUR),
            118.5344827586207)

    def test_convert_to_self_currency(self):

        for currency, name in CURRENCIES:
            self.assertEqual(
                ExchangeRate.convert(100, currency, currency), 100)

    def test_convert_with_printable_param_returns_printable_price(self):

        for currency, name in CURRENCIES:
            price = ExchangeRate.convert(
                100, currency, currency, printable=True)
            self.assertEqual(price, '100.00 %s' % name)

    def test_convert_with_format_price_param_returns_formatted_price(self):

        for currency, name in CURRENCIES:
            price = ExchangeRate.convert(
                100, currency, currency, format_price=True)
            self.assertEqual(price, '100.00')

    def test_convert_to_unknown_currency_raises_value_error(self):

        for currency, name in CURRENCIES:
            self.assertRaises(
                ValueError, ExchangeRate.convert, 100, currency, 5)

    def test_convert_from_unknown_currency_raises_value_error(self):

        for currency, name in CURRENCIES:
            self.assertRaises(
                ValueError, ExchangeRate.convert, 100, 5, currency)

    def test_set_currency_endpoint_changes_session_currency(self):

        for currency, name in CURRENCIES:

            url = '/currencies/set-currency/'

            response = self.client.post(url, {'currency': currency})

            self.assertEqual(response.status_code, 302)

            self.assertEqual(
                int(self.client.session[CURRENCY_SESSION_KEY]), currency)

    def test_get_currency_form_template_tag_returns_currency_form(self):

        factory = RequestFactory()

        request = factory.get('/')

        request.session = {CURRENCY_SESSION_KEY: CURRENCY_UAH}

        html = """
            {% load currencies %}
            {% get_currency_form as form %}
            {{ form }}
        """

        response = Template(html).render(RequestContext(request))

        self.assertIn('value="1" selected="selected">UAH', response)
        self.assertIn('value="2">USD', response)
        self.assertIn('value="3">EUR', response)
