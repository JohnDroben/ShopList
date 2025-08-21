from cart.models import Order

def order_statuses(request):
    return {'order_statuses': Order.STATUS_CHOICES}