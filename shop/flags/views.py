

def get_products_by_flag(request, flag_pk,
                         template_name='products/by_flag.html'):

    flag = get_object_or_404(ProductFlag, pk=flag_pk)

    context = {
        'flag': flag,
        'products': paginate(request, flag.products.all(), items_per_page=18)
    }

    return render(request, template_name, context)
