
from django.http import JsonResponse

from clothes.constants import DEFAULT_CLOTHES_SIZES
from clothes.forms import MaleSizeForm, FemaleSizeForm


def get_sizes(request, product_id):

    product = request.env.products.filter({'id': product_id}).get()

    return JsonResponse({
        'sizes': DEFAULT_CLOTHES_SIZES,
        'forms': _get_size_forms(product)
    })


def _get_size_forms(product, data=None):

    forms = []

    if product.has_male_size():
        forms.append(MaleSizeForm(data, prefix='male'))

    if product.has_female_size():
        forms.append(FemaleSizeForm(data, prefix='female'))
