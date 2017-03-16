
from django.apps import apps
from django.shortcuts import get_object_or_404, render

from pure_pagination import Paginator

from shop.products.filters import ProductFilter


def product_list(
        request, category_slug, category_pk, filter_class=ProductFilter):

    product_model = apps.get_model('products', 'Product')
    product_category_model = apps.get_model('products', 'ProductCategory')

    category = get_object_or_404(product_category_model, pk=category_pk)

    categories = category.get_descendants(include_self=True)

    products = product_model.objects.filter(category__in=categories)

    product_filter = filter_class(
        data=request.GET, queryset=products, category=category)

    paginator = Paginator(product_filter.qs, per_page=12, request=request)

    context = {
        'filter': product_filter,
        'category': category,
        'products': paginator.page(request.GET.get('page', 1))
    }

    return render(request, 'products/product_list.html', context)


def product_search(request):

    product_filter = ProductFilter(data=request.GET)

    paginator = Paginator(product_filter.qs, per_page=12, request=request)

    context = {
        'filter': product_filter,
        'products': paginator.page(request.GET.get('page', 1))
    }

    return render(request, 'products/search.html', context)


def product_info(request, product_slug, product_pk):

    product_model = apps.get_model('products', 'Product')

    product = get_object_or_404(product_model, pk=product_pk)

    return render(request, 'products/info.html', {'product': product})
