
from cart import defaults


class CartSettings(object):

    CART_PRODUCT_MODEL = defaults.CART_PRODUCT_MODEL

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + ['cart']

    @property
    def JAVASCRIPT(self):
        return super().JAVASCRIPT + (
            'cart.js',
        )

    @property
    def CONTEXT_PROCESSORS(self):
        return super().CONTEXT_PROCESSORS + [
            'cart.context_processors.cart'
        ]


default = CartSettings
