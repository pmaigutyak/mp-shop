
from modeltranslation.translator import translator

from clothes.models import CategoryProfile


translator.register(CategoryProfile, fields=['grid'])
