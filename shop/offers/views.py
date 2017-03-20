
from django.apps import apps
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_POST, require_GET

from shop.offers.forms import ProductPriceOfferForm
from shop.offers.lib import send_new_price_offer_notification


@require_GET
def get_price_offer_modal(request, product_pk):

    user = request.user

    Product = apps.get_model('products', 'Product')

    product = get_object_or_404(Product, pk=product_pk)

    if user.is_authenticated():
        profile = getattr(user, 'profile', None)
        initial = {
            'name': user.get_full_name(),
            'email': user.email,
            'mobile': profile.mobile if profile is not None else ''
        }
    else:
        initial = {}

    form = ProductPriceOfferForm(initial=initial)

    context = {
        'form': form,
        'product': product
    }

    return render(request, 'offers/price_offer_modal.html', context)


@require_POST
def send_price_offer(request, product_pk):

    Product = apps.get_model('products', 'Product')

    product = get_object_or_404(Product, pk=product_pk)

    form = ProductPriceOfferForm(request.POST)

    if form.is_valid():

        offer = form.save(commit=False)

        if request.user.is_authenticated():
            offer.user = request.user

        offer.product = product
        offer.save()

        send_new_price_offer_notification(offer)

        return HttpResponse(_('Offer successfully added'))

    context = {
        'form': form,
        'product': product
    }

    return render(request, 'offers/price_offer_form.html', context, status=400)
