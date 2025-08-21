from django.urls import path
from .views import manager_dashboard, order_detail, update_order_status


app_name = 'manager'


urlpatterns = [
    path('', manager_dashboard, name='manager_dashboard'),
    path('orders/<int:order_id>/', order_detail, name='manager_order_detail'),
    path('orders/<int:order_id>/update-status/', update_order_status, name='update_order_status'),
]