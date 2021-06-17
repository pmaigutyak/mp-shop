
from modeltranslation.translator import translator

from labels.models import ProductLabel


translator.register(ProductLabel, fields=['title'])
