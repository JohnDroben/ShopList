from django.urls import path
from .views import AboutView, DeliveryView

urlpatterns = [
    path('about/', AboutView.as_view(), name='about'),
    path('delivery/', DeliveryView.as_view(), name='delivery'),
]