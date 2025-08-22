from django.urls import path
from . import views
from .views import manager_dashboard, order_detail, update_order_status

app_name = 'manager'


urlpatterns = [
    path('', views.manager_dashboard, name='dashboard'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
]