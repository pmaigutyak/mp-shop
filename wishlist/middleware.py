
from wishlist.models import WishList


class WishListMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request.wishlist = WishList(request.user)

        return self.get_response(request)
