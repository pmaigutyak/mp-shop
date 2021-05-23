
from images import fields

from product_images.models import ProductImage


class ImagesFormField(fields.ImagesFormField):

    def __init__(self):
        super().__init__(ProductImage)
