
from django.db.models.signals import post_save

from basement.images.models import ImageRecord, ImageRecordMeta


class ProductImage(ImageRecord, metaclass=ImageRecordMeta):

    parent_model = 'products.Product'
    parent_field = 'product'

    class Meta(ImageRecord.Meta):
        db_table = 'products_images'


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
        watermark = WatermarkImage.get('product')
        watermark.process(instance.file.path)
    except Exception as e:
        pass


post_save.connect(_process_product_image, sender=ProductImage)
