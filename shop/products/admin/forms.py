
from copy import deepcopy

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from multiupload.fields import MultiFileField


class ProductForm(forms.ModelForm):

    images = MultiFileField(max_num=100, min_num=1, required=False)

    def __init__(self, *args, **kwargs):

        super(ProductForm, self).__init__(*args, **kwargs)

        fields = self.fields

        if self.instance.pk:
            self._build_attr_fields()

        if self.instance.pk is not None:
            fields.pop('category')

    @staticmethod
    def get_option_field_name(attr):
        return 'option_' + attr.full_slug

    def clean(self):
        data = super(ProductForm, self).clean()

        for attr in self.instance.attr.all():

            if attr.has_options:
                new_option = data.get(self.get_option_field_name(attr))

                if new_option:
                    option, c = attr.option_group.options.get_or_create(
                        option=new_option)
                    data[attr.full_slug] = option

        return data

    def _build_attr_fields(self):

        fields = self.fields = deepcopy(self.base_fields)

        for attr in self.instance.attr.all():

            fields[attr.full_slug] = self.get_attribute_field(attr)

            if attr.has_options:
                label = attr.name + unicode(_(' [New value]'))
                fields[self.get_option_field_name(attr)] = forms.CharField(
                    label=label, required=False)

            try:
                value = self.instance.attribute_values.get(
                    attribute=attr).value
            except ObjectDoesNotExist:
                pass
            else:
                self.initial[attr.full_slug] = value

    def _post_clean(self):

        for attr in self.instance.attr.all():

            if attr.full_slug in self.cleaned_data:
                value = self.cleaned_data[attr.full_slug]
                setattr(self.instance.attr, attr.slug, value)

        super(ProductForm, self)._post_clean()

    @staticmethod
    def get_attribute_field(attr):
        kwargs = {'label': attr.name, 'required': attr.required}

        if attr.type is ATTR_TYPE_SELECT:
            kwargs['queryset'] = attr.option_group.options.all()
            return forms.ModelChoiceField(**kwargs)

        return VALUE_FIELDS[attr.type].formfield(**kwargs)

    class Meta:
        model = Product
        fields = '__all__'


class ProductImageInline(SortableTabularInline):
    fields = ('preview', )
    readonly_fields = ['preview']
    model = ProductImage
    extra = 0
    max_num = 0


