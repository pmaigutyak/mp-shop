
import json

from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string

from clothes.constants import DEFAULT_CLOTHES_SIZES
from clothes.forms import MaleSizeForm, FemaleSizeForm
from clothes.storage import SizeStorage


def get_sizes(request):

    product = request.env.products.filter({
        'id': request.GET.get('product_id'),
        'is_visible': True
    }).get()

    data = request.POST or None

    storage = SizeStorage(request.session)

    sizes = storage.get(product.id)

    forms = {}

    if product.has_male_size():
        forms['male_form'] = MaleSizeForm(
            data,
            initial=sizes.get('male_form'),
            prefix='male')

    if product.has_female_size():
        forms['female_form'] = FemaleSizeForm(
            data,
            initial=sizes.get('female_form'),
            prefix='female')

    if request.method == 'POST':

        if all(f.is_valid() for f in forms.values()):
            storage.set(
                product.id,
                {name: form.cleaned_data for name, form in forms.items()}
            )
            return JsonResponse({})

        context = {'status_code': 403}
        context.update(forms)

        return render(request, 'clothes/modal.html', context)

    return JsonResponse({
        'sizes': DEFAULT_CLOTHES_SIZES,
        'modal': render_to_string('clothes/modal.html', forms, request)
    })
