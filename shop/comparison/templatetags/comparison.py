
from django import template


register = template.Library()


@register.assignment_tag(takes_context=True)
def get_comparison(context, session_key='comparison'):
    from shop.comparison import Comparison
    return Comparison(context['request'].session, session_key=session_key)
