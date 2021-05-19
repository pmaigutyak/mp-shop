
from django.apps import apps
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required

from wishlist.exceptions import ProductAlreadyAdded, ItemDoesNotExists


@login_required
def add(request, product_id):

    product = get_object_or_404(
        apps.get_model('products', 'Product'), id=product_id)

    try:
        request.wishlist.add(product)
    except ProductAlreadyAdded:
        message = _('{} already in your wish list')
        messages.success(request, message.format(product.name))
    else:
        message = _('{} added to wish list')
        messages.success(request, message.format(product.name))

    return redirect(request.GET.get('next', 'home'))


@login_required
def remove(request, product_id):

    product = get_object_or_404(
        apps.get_model('products', 'Product'), id=product_id)

    try:
        request.wishlist.remove(product_id)
    except ItemDoesNotExists:
        message = _('{} not in wish list')
        messages.error(request, message.format(product.name))
    else:
        message = _('{} was removed from wish list')
        messages.success(request, message.format(product.name))

    return redirect(request.GET.get('next', 'home'))
