from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from cart.models import Order


def manager_required(user):
    return user.groups.filter(name='Managers').exists() or user.is_staff


@login_required
@user_passes_test(manager_required)
def manager_dashboard(request):
    try:
        orders = Order.objects.all().order_by('-created_at')
        total_orders = orders.count()
        pending_orders = orders.filter(status='new').count()
        completed_orders = orders.filter(status='completed').count()

        context = {
            'orders': orders[:10],
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'completed_orders': completed_orders,
        }
        return render(request, 'manager/dashboard.html', context)
    except Exception as e:
        print(f"Error in manager dashboard: {e}")
        return render(request, 'error.html', {'error': 'Ошибка загрузки панели управления'})

@login_required
@user_passes_test(manager_required)
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'manager/order_detail.html', {'order': order})


@login_required
@user_passes_test(manager_required)
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')

        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            return JsonResponse({'success': True, 'new_status': order.get_status_display()})

    return JsonResponse({'success': False})