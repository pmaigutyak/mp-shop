
class OffersSettings(object):

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + [
            'offers'
        ]


default = OffersSettings
