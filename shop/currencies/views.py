
from django.http import JsonResponse
from django.views.generic import FormView

from shop.currencies.settings import CURRENCY_SESSION_KEY
from shop.currencies.forms import CurrencyForm


class SetCurrencyView(FormView):

    form_class = CurrencyForm

    http_method_names = ['post']

    def form_valid(self, form):

        currency = form.cleaned_data['currency']
        self.request.session[CURRENCY_SESSION_KEY] = currency

        return super(SetCurrencyView, self).form_valid(form)

    def form_invalid(self, form):
        return JsonResponse(form.errors.as_json())

    def get_success_url(self):
        return self.request.GET.get('next', '/')
