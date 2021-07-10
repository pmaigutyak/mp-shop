
class LiqPaySettings(object):

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + ['liqpay']


default = LiqPaySettings
