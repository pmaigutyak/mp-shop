
from django.forms import Field, ValidationError
from django.utils.translation import ugettext_lazy as _

from attributes.widgets import AttributesFormFieldWidget
from attributes.forms import AttributesForm


class AttributesFormField(Field):

    widget = AttributesFormFieldWidget
    form = None

    def init_form(self, *args, **kwargs):

        self.form = AttributesForm(*args, **kwargs)
        self.widget.form = self.form

    def clean(self, *args, **kwargs):

        if not self.form.is_valid():
            raise ValidationError(_('Form is invalid.'))

        return self.form.cleaned_data

    def commit(self, *args, **kwargs):
        return self.form.commit(*args, **kwargs)
