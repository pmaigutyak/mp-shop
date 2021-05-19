
from django.http import JsonResponse

from delivery.lib import search_warehouses, search_cities


def get_warehouses(request):

    warehouses = search_warehouses(
        request.GET.get('delivery_method'),
        request.GET.get('city'),
        request.GET.get('query'),
        limit=10)

    suggestions = [w.name for w in warehouses]

    return JsonResponse({
        'query': request.GET.get('query'),
        'suggestions': suggestions
    })


def get_cities(request):

    query = request.GET.get('query')

    suggestions = [str(c) for c in search_cities(query, limit=10)]

    return JsonResponse({
        'query': query,
        'suggestions': suggestions
    })
