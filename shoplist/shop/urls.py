from django.urls import path
from .views import ProductListView, ProductDetailView, CategoryView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]