from django.urls import path
from .views import CartView, add_to_cart, remove_from_cart, checkout, order_success

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('success/<int:order_id>/', order_success, name='order_success'),
]