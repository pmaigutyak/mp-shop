
from django.conf import settings

from modeltranslation.translator import TranslationOptions, translator


class ProductTranslationOptions(TranslationOptions):

    fields = ('title', 'description', )


class ProductCategoryTranslationOptions(TranslationOptions):

    fields = ('name', )


if 'shop.products' in settings.INSTALLED_APPS:

    from shop.products.models import Product, ProductCategory

    translator.register(Product, ProductTranslationOptions)
    translator.register(ProductCategory, ProductCategoryTranslationOptions)
