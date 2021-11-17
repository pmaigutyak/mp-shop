
from django import forms
from django.contrib import admin
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Hidden

from categories.models import Category


class ChangeCategoriesForm(forms.Form):

    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    value = forms.ModelChoiceField(
        label=Category._meta.verbose_name,
        queryset=Category.objects.all())

    should_data_be_replaced = forms.BooleanField(
        label=_('Replace existing categories'),
        initial=False,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('apply', _('Apply')))
        self.helper.add_input(Hidden('action', 'categories_change_action'))


def categories_change_action(modeladmin, request, queryset):

    data = request.POST

    apply = 'apply' in data

    initial = {
        '_selected_action': data.getlist(admin.ACTION_CHECKBOX_NAME)
    }

    form = ChangeCategoriesForm(
        data=data if apply else None,
        initial=initial if not apply else None)

    if apply and form.is_valid():

        category = form.cleaned_data['value']

        for instance in queryset:
            if form.cleaned_data['should_data_be_replaced']:
                instance.categories.set([category])
            else:
                instance.categories.add(category)

        messages.success(request, _('Changes saved'))

        return redirect(request.get_full_path())

    context = admin.site.each_context(request)

    context.update({
        'items': queryset,
        'form': form
    })

    return render(
        request,
        'change-attr-category-action.html',
        context)


categories_change_action.short_description = _('Change categories')
