
from django import template
from django.conf import settings


register = template.Library()


@register.inclusion_tag('offers/modal_js.html', name='offers_js')
def render_offers_js(obj, selector='[data-role=price-offer]'):
    return {
        'STATIC_URL': settings.STATIC_URL,
        'obj': obj,
        'selector': selector
    }
