from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Sum, F, Value
from django.db.models.functions import Concat
from .models import Category, Product
import csv
from django.http import HttpResponse


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = 'Количество товаров'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_status', 'image_preview', 'created_at')
    list_filter = ('category', 'created_at', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Цена и наличие', {
            'fields': ('price', 'stock', 'min_stock_level', 'is_active')
        }),
        ('Изображение', {
            'fields': ('image', 'image_preview')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['activate_products', 'deactivate_products', 'export_to_csv']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return "Нет изображения"

    image_preview.short_description = 'Превью'

    def stock_status(self, obj):
        if obj.stock == 0:
            return format_html('<span style="color: red;">Нет в наличии</span>')
        elif obj.stock <= obj.min_stock_level:
            return format_html('<span style="color: orange;">Мало ({})</span>', obj.stock)
        else:
            return format_html('<span style="color: green;">В наличии ({})</span>', obj.stock)

    stock_status.short_description = 'Статус наличия'

    def activate_products(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} товаров активировано.')

    activate_products.short_description = 'Активировать выбранные товары'

    def deactivate_products(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} товаров деактивировано.')

    deactivate_products.short_description = 'Деактивировать выбранные товары'

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'

        writer = csv.writer(response)
        writer.writerow(['Название', 'Категория', 'Цена', 'Остаток', 'Статус'])

        for product in queryset:
            writer.writerow([
                product.name,
                product.category.name,
                product.price,
                product.stock,
                'Активен' if product.is_active else 'Неактивен'
            ])

        return response

    export_to_csv.short_description = 'Экспорт в CSV'

    # Добавляем кастомное представление для быстрого добавления товара
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('quick-add/', self.admin_site.admin_view(self.quick_add_view), name='shop_product_quick_add'),
        ]
        return custom_urls + urls

    def quick_add_view(self, request):
        if request.method == 'POST':
            # Обработка быстрого добавления товара
            name = request.POST.get('name')
            category_id = request.POST.get('category')
            price = request.POST.get('price')

            if name and category_id and price:
                category = Category.objects.get(id=category_id)
                Product.objects.create(
                    name=name,
                    category=category,
                    price=price,
                    slug=slugify(name)[:50]  # Ограничиваем длину slug
                )
                messages.success(request, 'Товар успешно добавлен!')
                return redirect('admin:shop_product_changelist')
            else:
                messages.error(request, 'Заполните все обязательные поля!')

        categories = Category.objects.all()
        context = {
            'categories': categories,
            **self.admin_site.each_context(request),
        }
        return render(request, 'admin/shop/product/quick_add.html', context)