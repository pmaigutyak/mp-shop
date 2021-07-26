
from django import forms
from django.db.models import F
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class UpdatePricesForm(forms.Form):

    value = forms.IntegerField(label=_('Value'))

    type = forms.ChoiceField(
        label=_('Type'),
        choices=(
            ('percent', _('Percent %')),
            ('number', _('Number')),
        ))


def update_prices(self, request, queryset):

    apply = 'apply' in request.POST

    form = UpdatePricesForm(request.POST if apply else None)

    if apply and form.is_valid():

        value = form.cleaned_data['value']
        is_percent = form.cleaned_data['type'] == 'percent'

        for product in queryset:
            product.calculate_old_price(is_percent, value)
            product.calculate_retail_price(is_percent, value)
            product.save()

        messages.success(request, _('Prices updated'))
        return redirect(request.get_full_path())

    context = admin.site.each_context(request)
    context.update({
        'action_name': 'update_prices',
        'form': form,
        'object_list': queryset
    })

    return render(request, 'exchange/update_prices.html', context)


update_prices.short_description = _('Update prices')
