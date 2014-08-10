from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from accounts import profile
from cart import cart
from checkout import checkout
from checkout.forms import CheckoutForm
from checkout.models import Order, OrderItem


def show_checkout(request, template_name="checkout/checkout.html"):
    if cart.is_empty(request):
        cart_url = urlresolvers.reverse('show_cart')
        return HttpResponseRedirect(cart_url)

    error_message = ''
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            response = checkout.process(request)
            order_number = response.get('order_number', 0)
            error_message = response.get('message', '')
            if order_number:
                request.session['order_number'] = order_number
                receipt_url = urlresolvers.reverse('checkout_receipt')
                return HttpResponseRedirect(receipt_url)
        else:
            error_message = 'Correct the errors below'
    else:
        if request.user.is_authenticated():
            user_profile = profile.retrieve(request)
            form = CheckoutForm(instance=user_profile)
        else:
            form = CheckoutForm()
    ctx_dict = {
        'error_message': error_message,
        'form': form,
        'page_title': 'Checkout',
    }
    return render_to_response(template_name, ctx_dict, context_instance=RequestContext(request))


def checkout_receipt(request, template_name="checkout/receipt.html"):
    order_number = request.session.get('order_number', '')
    if order_number:
        order = Order.objects.filter(id=order_number)[0]
        order_items = OrderItem.objects.filter(order=order)
        del request.session['order_number']
        ctx_dict = {
            'order': order,
            'order_items': order_items,
        }
        return render_to_response(template_name, ctx_dict, context_instance=RequestContext(request))
    else:
        cart_url = urlresolvers.reverse('show_cart')
        return HttpResponseRedirect(cart_url)