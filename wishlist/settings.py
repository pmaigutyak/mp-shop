
class WishListSettings(object):

    @property
    def MIDDLEWARE(self):
        return super().MIDDLEWARE + [
            'wishlist.middleware.WishListMiddleware'
        ]

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + [
            'wishlist'
        ]


default = WishListSettings
