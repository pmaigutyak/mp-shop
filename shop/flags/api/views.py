
from django.shortcuts import render

from shop.flags.models import ProductFlag


def get_flags(request):

    flags = ProductFlag.objects.all().prefetch_related('products')

    return render(request, 'flags/api/flags.html', {'flags': flags})
