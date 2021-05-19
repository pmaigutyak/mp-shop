
from attributes import defaults


class AttributeSettings(object):

    ATTRIBUTES_CATEGORY_MODEL = defaults.ATTRIBUTES_CATEGORY_MODEL
    ATTRIBUTES_ENTRY_MODEL = defaults.ATTRIBUTES_ENTRY_MODEL

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + [
            'attributes'
        ]

default = AttributeSettings
