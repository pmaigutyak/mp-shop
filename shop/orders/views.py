
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

from shop.cart.lib import Cart

from shop.orders.forms import CheckoutForm
from shop.orders.lib import send_new_order_notifications


def checkout(request, form_class=CheckoutForm):

    user = request.user

    form_params = {'data': request.POST or None}

    if user.is_authenticated():

        profile = getattr(user, 'profile', None)

        form_params['initial'] = {
            'name': user.first_name,
            'email': user.email,
            'mobile': profile.mobile if profile is not None else ''
        }

    form = form_class(request, **form_params)

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
                price=product.price.default, quantity=item.qty)

        cart.clear()

        send_new_order_notifications(order)

        message = render_to_string(
            'cart/new_order_message.html', {'order': order})

        messages.success(request, mark_safe(message))

        return redirect('home')

    return render(request, 'cart/checkout.html', {'form': form})
