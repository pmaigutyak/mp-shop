
from django.conf import settings
from django.forms import Field, ValidationError
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from delivery.widgets import DeliveryFormFieldWidget
from delivery.forms import DeliveryForm


class DeliveryFormField(Field):

    widget = DeliveryFormFieldWidget
    form = None

    def init_form(self, *args, **kwargs):

        self.form = DeliveryForm(*args, **kwargs)
        self.widget.form = self.form

    def clean(self, *args, **kwargs):

        if not self.form.is_valid():
            raise ValidationError(_('Form is invalid.'))

        return self.form.cleaned_data

    def commit(self, *args, **kwargs):
        return self.form.commit(*args, **kwargs)

    def get_delivery_method(self):
        return self.form.cleaned_data['delivery_method']

    def get_address(self):
        return '{}, {}'.format(
            self.form.cleaned_data['warehouse'],
            self.form.cleaned_data['city'])

    @property
    def media(self):
        return render_to_string('delivery/media.html', {
            'STATIC_URL': settings.STATIC_URL,
            'form': self.form
        })

