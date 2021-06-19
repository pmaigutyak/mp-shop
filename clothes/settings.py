
class ClothesSettings(object):

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + ['clothes']

    @property
    def JAVASCRIPT(self):
        return super().JAVASCRIPT + (
            'clothes.js',
        )


default = ClothesSettings
