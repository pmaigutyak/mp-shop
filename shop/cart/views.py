
from django.apps import apps
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from shop.cart.lib import Cart
from shop.cart.forms import CartItemForm


def get_product_from_request(request):

    product_model = apps.get_model('products', 'Product')

    product_id = request.GET.get('product_id')

    return get_object_or_404(product_model, id=product_id)


def index(request, template_name='cart/index.html'):
    return render(request, template_name)


@require_POST
def add(request):

    product = get_product_from_request(request)

    cart = Cart(request.session)
    cart.add(product)

    return JsonResponse({
        'message': str(_('Added')),
        'total': cart.printable_default_total
    })


@require_POST
def remove(request):

    product = get_product_from_request(request)

    cart = Cart(request.session)
    cart.remove(product)

    return JsonResponse({
        'message': str(_('%s removed from card' % product.title)),
        'total': cart.printable_default_total
    })


@require_POST
def set_qty(request):

    product = get_product_from_request(request)

    form = CartItemForm(data=request.POST)

    if not form.is_valid():
        return JsonResponse(form.errors.as_json(), status=403)

    cart = Cart(request.session)
    cart.set_qty(product, form.cleaned_data['qty'])

    cart_item = cart.get_item(product)

    return JsonResponse({
        'message': str(_('%s removed from card' % product.title)),
        'subtotal': cart_item.printable_default_subtotal,
        'total': cart.printable_default_total
    })
