
from manufacturers.models import Manufacturer


class ManufacturerCollection(object):

    def get(self, name):

        if not hasattr(self, '_items'):

            qs = Manufacturer.objects\
                .values_list('pk', 'name')

            self._items = {name: pk for pk, name in qs}

        if not hasattr(self, '_adjustments'):
            qs = Manufacturer.objects\
                .exclude(new_name='')\
                .values_list('name', 'new_name')

            self._adjustments = {name: new_name for name, new_name in qs}

        if not name:
            return None

        try:
            name = self._adjustments[name]
        except KeyError:
            pass

        if name not in self._items:
            self._items[name] = Manufacturer.objects.create(name=name).pk

        return self._items[name]

    def get_once(self, name, last=False):

        m, created = Manufacturer.objects.get_or_create(name=name)

        if m.new_name and m.new_name != name and not last:
            return self.get_once(m.new_name, last=True)

        return m.pk
