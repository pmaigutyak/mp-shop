
from django.conf import settings


BUSINESS_TYPE = getattr(settings, 'BUSINESS_TYPE', None)

IS_CLOTHES_BUSINESS = BUSINESS_TYPE == 'clothes'
