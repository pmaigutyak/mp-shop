
from django.apps import apps
from django.db import transaction
from django.shortcuts import redirect, render, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from orders import utils
from orders.models import Order
from orders.forms import CheckoutForm


@transaction.atomic
def checkout(request):

    user = request.user
    initial = {'mobile': '+380'}

    if user.is_authenticated:
        initial.update({
            'first_name': user.first_name,
            'last_name': user.last_name
        })

    form = CheckoutForm(
        initial=initial,
        data=request.POST or None
    )

    if request.method == 'POST' and form.is_valid():

        cart = request.env.cart

        order = form.save(commit=False)

        order.delivery = form.fields['delivery'].get_delivery_method()
        order.address = form.fields['delivery'].get_address()

        if user.is_authenticated:
            order.user = request.user

        order.save()

        for item in cart.items:
            ordered_product = order.items.create(
                product_id=item.id,
                qty=item.qty,
                **item.price_values)

            if apps.is_installed('clothes'):
                request.env.clothes.create_size(ordered_product)

        cart.clear()

        utils.send_new_order_notifications(request, order)

        return redirect('home')

    return render(request, 'orders/checkout.html', {'form': form})


@staff_member_required
def resend_new_order_notifications(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    utils.send_new_order_notifications(request, order)
    return HttpResponse('Message sent')


@staff_member_required
def render_new_order_email(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = utils.get_new_order_context(order)
    context['debug'] = True
    return render(request, 'orders/new_order_email_for_manager.html', context)


@login_required
def get_history(request):
    context = {'order_items': request.user.order.all()}
    return render(request, 'orders/history.html', context)
