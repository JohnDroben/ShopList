from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render
from django.db.models import Count, Sum
from django.http import HttpResponse
import csv
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профиль'
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'order_count', 'total_spent',
                    'user_actions')  # Изменили на user_actions
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    actions = ['export_users_to_csv', 'make_staff', 'remove_staff']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            order_count=Count('order', distinct=True),
            total_spent=Sum('order__total_amount')
        )

    def order_count(self, obj):
        return obj.order_count

    order_count.short_description = 'Заказов'
    order_count.admin_order_field = 'order_count'

    def total_spent(self, obj):
        return f"{obj.total_spent or 0} ₽"

    total_spent.short_description = 'Потрачено'
    total_spent.admin_order_field = 'total_spent'

    def user_actions(self, obj):  # Переименовали метод
        return format_html(
            '<a href="/admin/auth/user/{}/change/">Редактировать</a> | '
            '<a href="/admin/auth/user/{}/delete/">Удалить</a>',
            obj.id, obj.id
        )

    user_actions.short_description = 'Действия'

    def make_staff(self, request, queryset):
        updated = queryset.update(is_staff=True)
        self.message_user(request, f'{updated} пользователей стали сотрудниками.')

    make_staff.short_description = 'Сделать сотрудниками'

    def remove_staff(self, request, queryset):
        updated = queryset.update(is_staff=False)
        self.message_user(request, f'{updated} пользователей больше не являются сотрудниками.')

    remove_staff.short_description = 'Убрать права сотрудника'

    def export_users_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'

        writer = csv.writer(response)
        writer.writerow(['Username', 'Email', 'Имя', 'Фамилия', 'Заказов', 'Потрачено', 'Статус'])

        for user in queryset:
            writer.writerow([
                user.username,
                user.email,
                user.first_name,
                user.last_name,
                user.order_count,
                user.total_spent or 0,
                'Сотрудник' if user.is_staff else 'Пользователь'
            ])

        return response

    export_users_to_csv.short_description = 'Экспорт пользователей в CSV'


# Перерегистрируем UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)