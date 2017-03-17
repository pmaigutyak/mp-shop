
from django.apps import apps


CURRENCY_UAH = 1


def create_category(name='Category name', parent=None):
    ProductCategory = apps.get_model('products', 'ProductCategory')
    category = ProductCategory(name=name)

    if parent is not None:
        category.parent = parent

    category.save()

    return category


def create_categories(count=3):

    categories = []

    for i in xrange(1, count + 1):
        categories.append(create_category('Category name %s' % i))

    return categories


def create_product(
        category, title='Product title', price_in_currency=0,
        currency=CURRENCY_UAH):

    Product = apps.get_model('products', 'Product')

    product = Product(
        category=category, title=title, price_in_currency=price_in_currency,
        currency=currency)

    product.save()

    return product


def create_products(category, count=3):

    products = []

    for i in xrange(1, count + 1):
        products.append(create_product(
            category=category, title='Product title %s' % i))

    return products
