
from django.conf import settings
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

    def __init__(self, category=None, *args, **kwargs):
        self._category = category
        super(ProductFilter, self).__init__(*args, **kwargs)

    @property
    def qs(self):

        qs = super(ProductFilter, self).qs

        if self._category is None:
            return qs

        categories = self._category.get_descendants(include_self=True)

        return qs.filter(category__in=categories)

    def get_search_fields(cls):

        fields = ['code']

        for language in dict(settings.LANGUAGES).keys():
            fields.append('title_%s' % language)
            fields.append('description_%s' % language)

        return fields

    def filter_query(self, queryset, name, value):
        return model_search(value, queryset, self.get_search_fields())

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
