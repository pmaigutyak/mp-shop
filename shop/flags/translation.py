
from modeltranslation.translator import translator, TranslationOptions

from shop.flags.models import ProductFlag


class ProductFlagTranslationOptions(TranslationOptions):

    fields = ('title', )


translator.register(ProductFlag, ProductFlagTranslationOptions)
