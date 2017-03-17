
from django.apps import apps
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import ugettext as _

from shop.comparison import Comparison


MAX_NUMBER_OF_COMPARISON_PRODUCTS = 4


def index(request):

    comparison = Comparison(request.session)

    category = _get_category_from_request(request)

    products = comparison.get_products(category)

    context = {
        'category': category,
        'products': products,
        'attributes': _format_attributes(category, products)
    }
    return render(request, 'comparison/index.html', context)


def add(request):

    product = _get_product_from_request(request)

    comparison = Comparison(request.session)

    max_number = MAX_NUMBER_OF_COMPARISON_PRODUCTS

    if len(comparison.get_products(product.category)) == max_number:
        message = _('Only %s products can be compared')
        messages.error(request, message % max_number)

    elif comparison.get_product(product.pk):
        message = _('%s already in comparison list')
        messages.error(request, message % product.title)

    else:
        comparison.add(product)

        message = _('%s added to comparison')
        messages.success(request, message % product.title)

    return redirect(request.GET.get('next', 'home'))


def remove(request):

    product = _get_product_from_request(request)

    comparison = Comparison(request.session)
    comparison.remove(product)

    message = _('%s removed from comparison')
    messages.success(request, message % product.title)

    return redirect(request.GET.get('next', 'home'))


def _format_attributes(category, products):
    attrs = []

    for attr in category.attributes.all():
        attrs.append({
            'name': attr.name,
            'values': [getattr(p.attr, attr.slug) for p in products]
        })

    return attrs


def _get_product_from_request(request):
    Product = apps.get_model('products', 'Product')
    return get_object_or_404(Product, pk=request.GET.get('product_pk'))


def _get_category_from_request(request):
    ProductCategory = apps.get_model('products', 'ProductCategory')
    return get_object_or_404(
        ProductCategory, pk=request.GET.get('category_pk'))
