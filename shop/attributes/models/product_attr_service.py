
class ProductAttributes(object):

    def __setstate__(self, state):
        self.__dict__ = state
        self.initialised = False

    def __init__(self, product):
        self.product = product
        self.initialised = False
        self._attrs = None

    def __getattr__(self, name):
        if not name.startswith('_') and not self.initialised:
            values = self.get_values().select_related('attr')
            for v in values:
                setattr(self, v.attribute.slug, v.value)
            self.initialised = True
            return getattr(self, name)
        return None

    def get_values(self):
        return self.product.attr_values.all()

    def get_value_by_attribute(self, attribute):
        return self.get_values().get(attribute=attribute)

    def all(self):
        if not self.product.pk:
            return []

        if not self._attrs:
            self._attrs = self.product.category.get_attributes()

        return self._attrs

    def get_attribute_by_slug(self, slug):
        return self.all().get(slug=slug)

    def __iter__(self):
        return iter(self.get_values())

    def save(self):
        for attribute in self.all():
            if hasattr(self, attribute.slug):
                value = getattr(self, attribute.slug)
                attribute.save_value(self.product, value)
