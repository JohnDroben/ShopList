def cart_summary(request):
    cart = request.session.get('cart', {})
    total_qty = sum(item['qty'] for item in cart.values())
    total_amount = sum(item['qty'] * float(item['price']) for item in cart.values())
    return {'cart_summary': {'total_qty': total_qty, 'total_amount': total_amount}}