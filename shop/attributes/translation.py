
from modeltranslation.translator import translator, TranslationOptions

from shop.attributes.models import ProductAttribute, AttributeOption


class ProductAttributeTranslationOptions(TranslationOptions):

    fields = ('name', )


class AttributeOptionTranslationOptions(TranslationOptions):

    fields = ('option', )


translator.register(ProductAttribute, ProductAttributeTranslationOptions)
translator.register(AttributeOption, AttributeOptionTranslationOptions)
