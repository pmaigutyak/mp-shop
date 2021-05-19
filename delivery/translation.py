
import sys

from modeltranslation.translator import translator

from delivery.models import Warehouse, Region, City, DeliveryMethod


translator.register(DeliveryMethod, fields=['name'])

if 'sync_translation_fields' not in sys.argv:
    translator.register(Region, fields=['name'])
    translator.register(City, fields=['name'])
    translator.register(Warehouse, fields=['name'])
