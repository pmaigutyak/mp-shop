
class LabelSettings(object):

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + ['labels']


default = LabelSettings
