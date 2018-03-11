
from django import template

from shop.stock import lib


register = template.Library()


@register.simple_tag
def get_availability_color(availability):
    return lib.get_availability_color(availability)
