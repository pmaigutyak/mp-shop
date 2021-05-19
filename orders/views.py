
from django.db import transaction
from django.shortcuts import redirect, render

from cart.lib import get_cart

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

        cart = get_cart(request)

        order = form.save(commit=False)

        order.delivery = form.fields['delivery'].get_delivery_method()
        order.address = form.fields['delivery'].get_address()

        if user.is_authenticated:
            order.user = request.user

        order.save()

        for item in cart.items:
            order.items.create(
                product_id=item.id,
                qty=item.qty,
                **item.price_values)

        cart.clear()

        send_new_order_notifications(request, order)

        return redirect('home')

    return render(request, 'orders/checkout.html', {'form': form})
