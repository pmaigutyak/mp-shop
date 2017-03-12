
from django import template


register = template.Library()


@register.assignment_tag
def get_product_flags():
    from shop.flags.models import ProductFlag
    return ProductFlag.objects.all().prefetch_related('products')
