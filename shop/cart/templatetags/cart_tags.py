
from django import template

from shop.cart.lib import Cart


register = template.Library()


@register.assignment_tag(takes_context=True)
def get_cart(context, session_key=None, cart_class=Cart):
    return cart_class(context['request'].session, session_key=session_key)
