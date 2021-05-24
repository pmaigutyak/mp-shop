
from basement.services import register_service

from attributes.forms import FilterForm


class AttributeService(object):

    @staticmethod
    @register_service('attrs')
    def factory(services, user, session, **kwargs):
        return AttributeService()

    def build_filter_form(self, category, data):
        return FilterForm(category, data)
