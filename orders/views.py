
from django.apps import apps
from django.db import transaction
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from orders.utils import send_new_order_notifications
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

        send_new_order_notifications(request, order)

        return redirect('home')

    return render(request, 'orders/checkout.html', {'form': form})


@login_required
def get_history(request):
    context = {'order_items': request.user.order.all()}
    return render(request, 'orders/history.html', context)
