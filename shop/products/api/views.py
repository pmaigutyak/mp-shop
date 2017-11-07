
from django.apps import apps
from django.shortcuts import render


def get_categories(request):

    root = request.GET.get('root', False)

    category_model = apps.get_model('products', 'ProductCategory')

    if root:
        categories = category_model.objects.root_nodes()
    else:
        categories = category_model.objects.all()

    context = {
        'categories': categories
    }

    return render(request, 'products/api/categories.html', context)
