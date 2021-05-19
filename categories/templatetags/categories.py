
from django import template
from django.apps import apps


register = template.Library()


@register.simple_tag()
def get_categories():
    return apps.get_model('categories', 'Category').objects.all()
