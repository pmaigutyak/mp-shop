
from django.http import JsonResponse
from django.template.loader import render_to_string

from clothes.constants import DEFAULT_CLOTHES_SIZES
from clothes.forms import MaleSizeForm, FemaleSizeForm


def get_sizes(request, product_id):

    product = request.env.products.filter({
        'id': product_id,
        'is_visible': True
    }).get()

    return JsonResponse({
        'sizes': DEFAULT_CLOTHES_SIZES,
        'form': _render_size_form(request, product)
    })


def _render_size_form(request, product, data=None):

    if product.has_male_size():
        male_form = MaleSizeForm(data, prefix='male')
    else:
        male_form = None

    if product.has_female_size():
        female_form = FemaleSizeForm(data, prefix='female')
    else:
        female_form = None

    return render_to_string('clothes/form.html', {
        'male_form': male_form,
        'female_form': female_form
    }, request)
