
from django.apps import apps
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required

from shop.wishlist.models import WishListItem


@login_required
def index(request):
    context = {'wishlist_items': request.user.wishlist_items.all()}
    return render(request, 'wishlist/index.html', context)


@login_required
def add(request):

    Product = apps.get_model('products', 'Product')

    product = get_object_or_404(
        Product, pk=request.GET.get('product_pk'))

    if WishListItem.objects.filter(product=product).exists():
        message = _('%s already in your wish list')
        messages.success(request, message % product.title)

    else:
        WishListItem.objects.create(
            user=request.user, product=product, product_title=product.title,
            qty=request.GET.get('qty', 1))

        message = _('%s addet to wish list')
        messages.success(request, message % product.title)

    return redirect(request.GET.get('next', 'home'))


@login_required
def remove(request):

    item = get_object_or_404(WishListItem, pk=request.GET.get('pk'))
    item.delete()

    message = _('%s was removed from wish list')
    messages.success(request, message % item.product_title)

    return redirect(request.GET.get('next', 'home'))
