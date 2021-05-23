
from basement.views import render_view


def get_product_page_context(request, product_id, queryset=None):

    products = request.env.products

    if queryset is None:
        queryset = products.filter({
            'is_visible': True,
            'id': product_id,
        }).select_related(
            'category',
            'availability'
        )

    product = queryset.get()

    products.add_to_history(product_id)

    related_products = queryset.for_category(product.category)

    return {
        'object': product,
        'recently_viewed_products': (
            products.get_from_history(queryset, count=4)),
        'related_products': products.get_related(
            related_products, product_id, count=4)
    }


@render_view('products/product.html')
def get_product(request, product_id, **kwargs):
    return get_product_page_context(request, product_id)
