from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponse
import csv
from django.db.models import Sum, F, Count
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'total_price')

    def total_price(self, obj):
        return obj.quantity * obj.price

    total_price.short_description = 'Общая стоимость'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_info', 'status_badge', 'total_amount', 'created_at', 'order_actions')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'user__username', 'user__email', 'name', 'email')
    readonly_fields = ('created_at', 'updated_at', 'total_amount_calculated')
    inlines = [OrderItemInline]
    actions = ['mark_as_processing', 'mark_as_completed', 'export_orders_to_csv']

    fieldsets = (
        (None, {
            'fields': ('user', 'status')
        }),
        ('Информация о клиенте', {
            'fields': ('name', 'email', 'address')
        }),
        ('Финансы', {
            'fields': ('total_amount_calculated',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def user_info(self, obj):
        if obj.user:
            return f"{obj.user.username} ({obj.user.email})"
        return f"{obj.name} ({obj.email})"

    user_info.short_description = 'Пользователь'

    def status_badge(self, obj):
        status_colors = {
            'new': 'blue',
            'processing': 'orange',
            'completed': 'green',
            'cancelled': 'red'
        }
        color = status_colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 10px;">{}</span>',
            color, obj.get_status_display()
        )

    status_badge.short_description = 'Статус'

    def total_amount_calculated(self, obj):
        return obj.total_amount

    total_amount_calculated.short_description = 'Общая сумма'

    def order_actions(self, obj):
        return format_html(
            '<a href="/admin/cart/order/{}/change/">Редактировать</a> | '
            '<a href="/admin/cart/order/{}/delete/">Удалить</a>',
            obj.id, obj.id
        )

    order_actions.short_description = 'Действия'

    def mark_as_processing(self, request, queryset):
        updated = queryset.update(status='processing')
        self.message_user(request, f'{updated} заказов помечено как "В обработке".')

    mark_as_processing.short_description = 'Пометить как "В обработке"'

    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} заказов помечено как "Завершено".')

    mark_as_completed.short_description = 'Пометить как "Завершено"'

    def export_orders_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Клиент', 'Email', 'Статус', 'Сумма', 'Дата создания'])

        for order in queryset:
            writer.writerow([
                order.id,
                order.name,
                order.email,
                order.get_status_display(),
                order.total_amount,
                order.created_at.strftime('%Y-%m-%d %H:%M')
            ])

        return response

    export_orders_to_csv.short_description = 'Экспорт заказов в CSV'

    # Добавляем кастомное представление для аналитики заказов
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('analytics/', self.admin_site.admin_view(self.analytics_view), name='cart_order_analytics'),
        ]
        return custom_urls + urls

    def analytics_view(self, request):
        # Статистика по заказам
        total_orders = Order.objects.count()
        total_revenue = Order.objects.aggregate(total=Sum(F('items__quantity') * F('items__price')))['total'] or 0

        # Статистика по статусам
        status_stats = Order.objects.values('status').annotate(
            count=Count('id'),
            revenue=Sum(F('items__quantity') * F('items__price'))
        )

        # Последние заказы
        recent_orders = Order.objects.select_related('user').prefetch_related('items').order_by('-created_at')[:10]

        context = {
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'status_stats': status_stats,
            'recent_orders': recent_orders,
            **self.admin_site.each_context(request),
        }
        return render(request, 'admin/cart/order/analytics.html', context)