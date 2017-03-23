
from django.shortcuts import get_object_or_404, render

from pure_pagination import Paginator

from shop.flags.models import ProductFlag


def get_products_by_flag(request, flag_pk):

    flag = get_object_or_404(ProductFlag, pk=flag_pk)

    paginator = Paginator(flag.products.visible(), per_page=18, request=request)

    context = {
        'flag': flag,
        'products': paginator.page(request.GET.get('page', 1))
    }

    return render(request, 'products/by_flag.html', context)
