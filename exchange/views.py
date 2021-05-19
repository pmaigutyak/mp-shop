
from django.shortcuts import redirect, HttpResponse
from django.views.decorators.http import require_POST

from exchange.constants import CURRENCY_SESSION_KEY
from exchange.forms import CurrencyForm


@require_POST
def set_currency(request):

    form = CurrencyForm(request.POST)

    if not form.is_valid():
        return HttpResponse(str(form.errors))

    currency = form.cleaned_data['currency']

    request.session[CURRENCY_SESSION_KEY] = currency

    return redirect(request.GET.get('next', 'home'))