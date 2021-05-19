
class ExchangeSettings(object):

    @property
    def INSTALLED_APPS(self):
        apps = super().INSTALLED_APPS + ['exchange']

        if 'solo' not in apps:
            apps.append('solo')

        return apps

    @property
    def CONTEXT_PROCESSORS(self):
        return super().CONTEXT_PROCESSORS + [
            'exchange.context_processors.currencies'
        ]


default = ExchangeSettings
