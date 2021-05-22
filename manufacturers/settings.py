
class ManufacturerSettings(object):

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + [
            'manufacturers'
        ]

default = ManufacturerSettings
