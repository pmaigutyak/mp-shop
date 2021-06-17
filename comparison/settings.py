
from comparison import defaults


class ComparisonSettings(object):

    COMPARISON_CATEGORY_MODEL = defaults.COMPARISON_CATEGORY_MODEL
    COMPARISON_PRODUCT_MODEL = defaults.COMPARISON_PRODUCT_MODEL

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + ['comparison']

    @property
    def MIDDLEWARE(self):
        return super().MIDDLEWARE + [
            'comparison.middleware.ComparisonMiddleware'
        ]

    @property
    def JAVASCRIPT(self):
        return super().JAVASCRIPT + (
            'comparison/comparison.js',
        )

default = ComparisonSettings
