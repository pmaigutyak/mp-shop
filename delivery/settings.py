
class DeliverySettings(object):

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + [
            'delivery'
        ]

    @property
    def DATABASES(self):
        databases = super().DATABASES
        databases['delivery'] = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'mp',
            'USER': 'dev'
        }
        return databases

    @property
    def DATABASE_ROUTERS(self):
        return super().DATABASE_ROUTERS + [
            'delivery.routers.DeliveryRouter'
        ]
