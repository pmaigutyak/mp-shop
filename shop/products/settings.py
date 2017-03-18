
from django.conf import settings


IS_CKEDITOR_ENABLED_FOR_PRODUCT_DESCRIPTION = getattr(
    settings, 'IS_CKEDITOR_ENABLED_FOR_PRODUCT_DESCRIPTION', False)
