
from django.apps import apps
from django.shortcuts import get_object_or_404, render
from django.views.generic.detail import DetailView

from pure_pagination import Paginator

from shop.products.forms import SearchProductForm


def product_list(request, category_slug, category_pk,
                 search_form_class=SearchProductForm):

    Product = apps.get_model('products', 'Product')
    ProductCategory = apps.get_model('products', 'ProductCategory')

    category = get_object_or_404(ProductCategory, pk=category_pk)

    categories = category.get_descendants(include_self=True)

    products = Product.visible.filter(category__in=categories)

    form = search_form_class(
        data=request.GET, products=products, category=category)

    paginator = Paginator(form.get_objects(), per_page=12, request=request)

    context = {
        'search_form': form,
        'category': category,
        'products': paginator.page(request.GET.get('page', 1))
    }

    return render(request, 'products/product_list.html', context)


def product_search(request):

    Product = apps.get_model('products', 'Product')

    form = SearchProductForm(Product.visible.all(), data=request.GET)

    paginator = Paginator(form.get_objects(), per_page=12, request=request)

    context = {
        'search_form': form,
        'products': paginator.page(request.GET.get('page', 1))
    }

    return render(request, 'products/search.html', context)


class ProductInfoView(DetailView):

    model = apps.get_model('products', 'Product')

    pk_url_kwarg = 'product_pk'

    context_object_name = 'product'

    template_name = 'products/info.html'

    def get_queryset(self):
        return self.model.visible.all()

    def update_viewed_products(self, count=6):

        request = self.request

        product_pk = self.kwargs.get(self.pk_url_kwarg)

        product_pks = request.session.get('viewed_product_pks', [])

        if product_pk in product_pks:
            product_pks.remove(product_pk)

        product_pks.insert(0, product_pk)

        if len(product_pks) > count:
            product_pks = product_pks[:count]

        request.session['viewed_product_pks'] = product_pks

        return product_pks

    def get_viewed_products(self):
        viewed_product_pks = self.update_viewed_products()
        return self.get_queryset().filter(pk__in=viewed_product_pks)

    def get_context_data(self, **kwargs):
        context = super(ProductInfoView, self).get_context_data(**kwargs)
        context['recently_viewed_products'] = self.get_viewed_products()
        return context
