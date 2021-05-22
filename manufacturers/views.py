
from django.http.response import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

from model_search import model_search

from manufacturers.models import Manufacturer


@staff_member_required
def manufacturer_autocomplete(request):

    query = request.GET.get('query')

    suggestions = [w.name for w in _search_manufacturers(query, limit=10)]

    return JsonResponse({
        'query': query,
        'suggestions': suggestions
    })


def _search_manufacturers(query, limit=None):

    if not query:
        return []

    queryset = model_search(query, Manufacturer.objects.all(), ['name'])

    if limit is not None:
        return queryset[:limit]

    return queryset
