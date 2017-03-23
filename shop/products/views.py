
from django.apps import apps
from django.shortcuts import get_object_or_404, render

from pure_pagination import Paginator

from shop.products.forms import SearchProductForm


def product_list(request, category_slug, category_pk,
                 search_form_class=SearchProductForm):

    Product = apps.get_model('products', 'Product')
    ProductCategory = apps.get_model('products', 'ProductCategory')

    category = get_object_or_404(ProductCategory, pk=category_pk)

    categories = category.get_descendants(include_self=True)

    products = Product.visible.filter(category__in=categories)

    form = search_form_class(
        data=request.GET, products=products, category=category)

    paginator = Paginator(form.get_objects(), per_page=12, request=request)

    context = {
        'search_form': form,
        'category': category,
        'products': paginator.page(request.GET.get('page', 1))
    }

    return render(request, 'products/product_list.html', context)


def product_search(request):

    Product = apps.get_model('products', 'Product')

    form = SearchProductForm(Product.visible.all(), data=request.GET)

    paginator = Paginator(form.get_objects(), per_page=12, request=request)

    context = {
        'search_form': form,
        'products': paginator.page(request.GET.get('page', 1))
    }

    return render(request, 'products/search.html', context)


def product_info(request, product_slug, product_pk):

    Product = apps.get_model('products', 'Product')

    product = get_object_or_404(Product.visible.all(), pk=product_pk)

    return render(request, 'products/info.html', {'product': product})
