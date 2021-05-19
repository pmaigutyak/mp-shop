
from modeltranslation.translator import translator

from attributes.models import Attribute, AttributeOption


translator.register(Attribute, fields=['name'])
translator.register(AttributeOption, fields=['name'])
