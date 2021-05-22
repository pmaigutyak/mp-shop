
class ClothesSettings(object):

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + ['clothes']


default = ClothesSettings
