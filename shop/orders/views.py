
from django.apps import apps
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

from easy_pdf.views import PDFTemplateView

from shop.cart.lib import Cart

from shop.orders.settings import ORDER_INVOICE_MOBILE, ORDER_INVOICE_EMAIL
from shop.orders.forms import CheckoutForm
from shop.orders.lib import send_new_order_notifications


def checkout(request, form_class=CheckoutForm):

    user = request.user

    form_params = {'data': request.POST or None}

    if user.is_authenticated():

        profile = getattr(user, 'profile', None)

        form_params['initial'] = {
            'name': user.first_name,
            'surname': user.last_name,
            'email': user.email,
            'mobile': profile.mobile if profile is not None else ''
        }

    form = form_class(**form_params)

    if request.method == 'POST' and form.is_valid():

        cart = Cart(request.session)

        order = form.save(commit=False)

        if user.is_authenticated():
            order.user = user

        order.save()

        for item in cart.items:
            product = item.product
            order.products.create(
                parent=product, title=product.title,
                price=product.price.default, qty=item.qty)

        cart.clear()

        send_new_order_notifications(order)

        message = render_to_string(
            'orders/new_order_message.html', {'order': order})

        messages.success(request, mark_safe(message))

        return redirect('home')

    return render(request, 'orders/checkout.html', {'form': form})


@login_required
def order_history(request):
    context = {'order_items': request.user.order.all()}
    return render(request, 'orders/history.html', context)


class OrderInvoiceDownloadView(PDFTemplateView):

    template_name = 'orders/invoice.html'

    def get_context_data(self, **kwargs):
        context = super(
            OrderInvoiceDownloadView, self).get_context_data(**kwargs)

        Order = apps.get_model('orders', 'Order')

        user = self.request.user

        order_params = {'pk': self.kwargs.get('pk')}

        if not user.is_superuser:
            order_params['user'] = user

        context.update({
            'site': Site.objects.get_current(),
            'mobile': ORDER_INVOICE_MOBILE,
            'email': ORDER_INVOICE_EMAIL,
            'order': get_object_or_404(Order, **order_params)
        })

        return context
