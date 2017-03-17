
from django.conf import settings
from django.test import TestCase

from mpshop.products.test_helpers import (
    create_category, create_categories, create_products)


class ProductTest(TestCase):

    def setUp(self):
        self.language_code = settings.LANGUAGE_CODE

    def test_list_contain_product_titles(self):

        category = create_category(name='Test category')

        products = create_products(category)

        url = '/%s/products/category/test_category_1/' % self.language_code

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        for product in products:
            self.assertContains(response, product.title)

    def test_list_has_next_page_url(self):

        category = create_category(name='Test category')

        create_products(category, count=18)

        url = '/%s/products/category/test_category_1/' % (
            self.language_code)

        response = self.client.get(url)

        self.assertContains(response, url + '?page=2')

    def test_list_has_previous_page_url(self):

        category = create_category(name='Test category')

        create_products(category, count=18)

        url = '/%s/products/category/test_category_1/' % (
            self.language_code)

        response = self.client.get(url + '?page=2')

        self.assertContains(response, url + '?page=1')


class ProductCategoryTest(TestCase):

    def setUp(self):
        self.language_code = settings.LANGUAGE_CODE

    def test_category_slug(self):

        category = create_category(name='Test category')

        self.assertEqual(category.slug, 'test_category')

    def test_category_full_slug(self):

        parent = create_category(name='Parent')

        category = create_category(name='Child', parent=parent)

        self.assertEqual(category.full_slug, 'parent/child')

    def test_category_full_name(self):

        parent = create_category(name='Parent')

        category = create_category(name='Child', parent=parent)

        self.assertEqual(category.full_name, 'Parent > Child')

    def test_category_absolute_url(self):

        parent = create_category(name='Parent')

        category = create_category(name='Child', parent=parent)

        self.assertEqual(category.get_absolute_url(),
                         '/uk/products/category/parent/child_2/')

    def test_list_contain_category_names(self):

        categories = create_categories(count=3)

        response = self.client.get('/%s/products/' % self.language_code)

        self.assertEqual(response.status_code, 200)

        for category in categories:
            self.assertContains(response, category.name)
