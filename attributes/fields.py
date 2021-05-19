
from basement.fields import FormField

from attributes.widgets import AttributesFormFieldWidget
from attributes.forms import AttributesForm


class AttributesFormField(FormField):

    widget = AttributesFormFieldWidget

    def _build_form(self, *args, **kwargs):
        return AttributesForm(*args, **kwargs)
