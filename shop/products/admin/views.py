
from django.apps import apps
from django.shortcuts import render


def product_statistic(request):

    request.current_app = 'products'

    Product = apps.get_model('products', 'Product')
    ProductCategory = apps.get_model('products', 'ProductCategory')

    context = {
        'category_count': ProductCategory.objects.count(),
        'product_count': Product.objects.count()
    }

    return render(request, 'products/admin/statistic.html', context)
