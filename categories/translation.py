
from modeltranslation.translator import translator

from categories.models import Category


translator.register(Category, fields=['name', 'title', 'description'])
