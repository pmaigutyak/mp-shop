
from django.test import TestCase
from django.test.client import RequestFactory
from django.template import Template, RequestContext

from shop.products.test_helpers import create_category, create_products

from shop.flags.models import ProductFlag


class FlagsTest(TestCase):

    def setUp(self):

        self.flags = create_flags
        self.products = create_products(category=create_category(), count=2)

    def test_set_currency_endpoint_changes_session_currency(self):

        url = '/currencies/set-currency/'

        response = self.client.post(url, {'currency': currency})

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            int(self.client.session[CURRENCY_SESSION_KEY]), currency)

    # def test_get_currency_form_template_tag_returns_currency_form(self):
    #
    #     factory = RequestFactory()
    #
    #     request = factory.get('/')
    #
    #     request.session = {CURRENCY_SESSION_KEY: CURRENCY_UAH}
    #
    #     html = """
    #         {% load currencies %}
    #         {% get_currency_form as form %}
    #         {{ form }}
    #     """
    #
    #     response = Template(html).render(RequestContext(request))
    #
    #     self.assertIn('value="1" selected="selected">UAH', response)
    #     self.assertIn('value="2">USD', response)
    #     self.assertIn('value="3">EUR', response)
