
from django.db.models.signals import post_save

from images.models import ImageRecord, ImageRecordMeta
from watermarks.utils import insert_watermark


class ProductImage(ImageRecord, metaclass=ImageRecordMeta):

    parent_model = 'products.Product'
    parent_field = 'product'

    class Meta(ImageRecord.Meta):
        db_table = 'products_image'


def _process_product_image(sender, instance, created, **kwargs):

    if not created:
        return

    # image = Image.open(instance.file.path)
    # width, height = image.size
    #
    # if width > height:
    #     image = image.rotate(-90, expand=1)
    #
    # image.thumbnail(MAX_SIZE, Image.ANTIALIAS)
    #
    # image.save(instance.file.path)

    try:
        insert_watermark('product', instance.file.path)
    except Exception as e:
        pass


post_save.connect(_process_product_image, sender=ProductImage)
