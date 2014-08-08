from cart import cart
from checkout import credit_card_agent
from checkout.forms import CheckoutForm
from checkout.models import Order, OrderItem


def process(request):
    # Transaction results
    APPROVED = '1'
    DECLINED = '2'
    ERROR = '3'
    HELD_FOR_REVIEW = '4'

    card_num = request.POST.get('credit_card_number', '')
    exp_month = request.POST.get('credit_card_expire_month', '')
    exp_year = request.POST.get('credit_card_expire_year', '')
    exp_date = exp_month + exp_year
    cvv = request.POST.get('credit_card_cvv', '')
    amount = cart.cart_subtotal(request)

    results = {}
    response = credit_card_agent.do_auth_capture(amount=amount, card_num=card_num, exp_date=exp_date, card_cvv=cvv)
    if response[0] == APPROVED:
        transaction_id = response[6]
        order = create_order(request, transaction_id)
        results = {
            'order_number': order.id,
            'message':'',
        }
    elif response[0] == DECLINED:
        results = {
            'order_number': 0,
            'message': 'There is a problem with your credit card.',
        }
    elif response[0] == ERROR or response[0] == HELD_FOR_REVIEW:
        results = {
            'order_number': 0,
            'message': 'Error processing your order.',
        }
    return results


def create_order(request, transaction_id):
    order = Order()
    checkout_form = CheckoutForm(request.POST, instance=order)
    order = checkout_form.save(commit=False)
    order.transaction_id = transaction_id
    order.ip_address = request.META.get('REMOTE_ADDR')
    order.user = None
    order.status = Order.SUBMITTED
    order.save()

    # if the order save succeeded
    if order.pk:
        cart_items = cart.get_cart_items(request)
        for ci in cart_items:
            # create order item for each cart item
            oi = OrderItem()
            oi.order = order
            oi.quantity = ci.quantity
            oi.price = ci.price # now using @property
            oi.product = ci.product
            oi.save()
        # all set, empty cart
        cart.empty_cart(request)

    # return the new order object
    return order