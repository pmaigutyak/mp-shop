
from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from django_filters import FilterSet, CharFilter, ChoiceFilter

from model_search import model_search


class ProductFilter(FilterSet):

    ORDER_BY_NEWEST = 'newest'
    ORDER_BY_A_TO_Z = 'title'
    ORDER_BY_Z_TO_A = '-title'

    ORDER_CHOICES = (
        (ORDER_BY_NEWEST, _('Newest')),
        (ORDER_BY_A_TO_Z, _('A-Z')),
        (ORDER_BY_Z_TO_A, _('Z-A')),
    )

    query = CharFilter(label=_('Query'), method='filter_query')

    order_by = ChoiceFilter(
        label=_('Order by'), choices=ORDER_CHOICES, method='filter_order_by',
        initial=ORDER_BY_NEWEST
    )

    def filter_query(self, queryset, name, value):
        return model_search(value, queryset, ['title', 'code', 'description'])

    def filter_order_by(self, queryset, name, value):

        if not value:
            return queryset

        if value == self.ORDER_BY_NEWEST:
            return queryset.order_by('-id')

        if value == self.ORDER_BY_A_TO_Z:
            return queryset.order_by('title')

        if value == self.ORDER_BY_Z_TO_A:
            return queryset.order_by('-title')

    class Meta:
        model = apps.get_model('products', 'Product')
        fields = ['query', 'order_by']
