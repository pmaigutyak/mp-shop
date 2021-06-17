
from django.shortcuts import render, get_object_or_404

from pagination import paginate

from labels.models import ProductLabel


def get_labels(request):
    return render(request, 'labels/list.html', {
        'labels': ProductLabel.objects.all()
    })


def get_products_by_label(request, label_id):

    label = get_object_or_404(ProductLabel, id=label_id)

    return render(request, 'labels/products.html', {
        'label': label,
        'page_obj': paginate(request, label.products.visible())
    })
