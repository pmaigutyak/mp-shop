
from random import randint


def add_product_to_history(request, product_id):

    product_ids = request.session.get('PRODUCT_HISTORY', [])

    if product_id in product_ids:
        product_ids.remove(product_id)

    product_ids.insert(0, product_id)

    request.session['PRODUCT_HISTORY'] = product_ids


def get_products_from_history(request, queryset, count=6):

    ids = request.session.get('PRODUCT_HISTORY', [])[:count]

    if not ids:
        return []

    return queryset.filter(id__in=ids)


def get_related_products(queryset, product_id, count=6):

    index = 0

    related_products = queryset.exclude(pk=product_id)

    related_products_count = len(related_products)

    if related_products_count:

        if related_products_count > count:
            index = randint(0, related_products_count - count)

        return related_products[index:index + count]

    return []
