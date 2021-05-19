
class ProductImagesSettings(object):

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + [
            'product_images'
        ]


default = ProductImagesSettings
