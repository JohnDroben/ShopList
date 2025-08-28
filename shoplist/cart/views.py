from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.conf import settings
from shop.models import Product
from .forms import CheckoutForm
from .models import Order, OrderItem
from yookassa import Configuration, Payment
import uuid


class CartView(TemplateView):
    template_name = 'cart/cart.html'


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get(settings.CART_SESSION_ID, {})
    key = str(product_id)

    if key not in cart:
        cart[key] = {'name': product.name, 'price': float(product.price), 'qty': 0}

    cart[key]['qty'] += 1
    request.session[settings.CART_SESSION_ID] = cart

    # Редирект на страницу товара вместо корзины
    return redirect('product_detail', slug=product.slug)


def remove_from_cart(request, product_id):
    cart = request.session.get(settings.CART_SESSION_ID, {})
    key = str(product_id)

    if key in cart:
        del cart[key]
        request.session[settings.CART_SESSION_ID] = cart

    return redirect('cart')


def checkout(request):
    cart = request.session.get(settings.CART_SESSION_ID, {})

    if not cart:
        return redirect('cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
         try:
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
            )


            for pid, item in cart.items():
                product = Product.objects.get(pk=int(pid))
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['qty'],
                    price=item['price']
                )

            # Очистка корзины и перенаправление на оплату
            request.session[settings.CART_SESSION_ID] = {}
            return redirect('order_success', order_id=order.id)
         except Exception as e:
            # Логирование ошибки
            print(f"Error creating order: {e}")
            return render(request, 'cart/checkout.html', {
                'form': form,
                'cart': cart,
                'error': 'Произошла ошибка при оформлении заказа'
            })
    else:
        form = CheckoutForm()

    return render(request, 'cart/checkout.html', {'form': form, 'cart': cart})

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'cart/success.html', {'order': order})


# Настройка конфигурации ЮKassa
Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


def create_payment(request, order_id, amount):
    cart = request.session.get(settings.CART_SESSION_ID, {})
    total_amount = sum(item['qty'] * float(item['price']) for item in cart.values())

    payment = Payment.create({
        "amount": {
            "value": f"{total_amount:.2f}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"{request.scheme}://{request.get_host()}/cart/success/{order_id}/"
        },
        "capture": True,
        "description": f"Заказ #{order_id}"
    }, uuid.uuid4())

    return redirect(payment.confirmation.confirmation_url)