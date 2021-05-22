
from django.test import TestCase

from manufacturers.models import Manufacturer
from manufacturers.utils import ManufacturerCollection


class ManufacturerCollectionTestCase(TestCase):

    def setUp(self):
        self.manufacturer_1 = Manufacturer.objects.create(
            name='m1')

        self.manufacturer_2 = Manufacturer.objects.create(
            name='m2', new_name='m1')

        self.manufacturer_3 = Manufacturer.objects.create(
            name='m3')

        self.manufacturer_4 = Manufacturer.objects.create(
            name='m4', new_name='m4')

        self.manufacturer_5 = Manufacturer.objects.create(
            name='m5', new_name='m6')

        self.manufacturer_6 = Manufacturer.objects.create(
            name='m6', new_name='m5')

        self.collection = ManufacturerCollection()

    def test_collection_returns_correct_manufacturer(self):

        self.assertEqual(self.collection.get('m1'), self.manufacturer_1.pk)
        self.assertEqual(self.collection.get('m2'), self.manufacturer_1.pk)

        self.assertEqual(
            self.collection.get_once('m1'), self.manufacturer_1.pk)

        self.assertEqual(
            self.collection.get_once('m2'), self.manufacturer_1.pk)

        self.assertEqual(
            self.collection.get_once('m4'), self.manufacturer_4.pk)

        self.assertEqual(
            self.collection.get_once('m5'), self.manufacturer_6.pk)
