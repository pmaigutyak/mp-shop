

class CategorySettings(object):

    @property
    def INSTALLED_APPS(self):
        apps = super().INSTALLED_APPS + ['categories']

        if 'mptt' not in apps:
            apps.append('mptt')

        return apps


default = CategorySettings
