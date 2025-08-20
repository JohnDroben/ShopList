from django.contrib.auth.models import User, Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from shop.models import Category, Product
from manager.models import ManagerProfile


class Command(BaseCommand):
    help = 'Create demo categories, products and test users'

    def handle(self, *args, **options):
        # Создание группы менеджеров
        managers_group, created = Group.objects.get_or_create(name='Managers')
        if created:
            # Добавляем права на управление товарами и категориями
            content_type = ContentType.objects.get_for_model(Product)
            permissions = Permission.objects.filter(content_type=content_type)
            for perm in permissions:
                managers_group.permissions.add(perm)

            content_type = ContentType.objects.get_for_model(Category)
            permissions = Permission.objects.filter(content_type=content_type)
            for perm in permissions:
                managers_group.permissions.add(perm)

            self.stdout.write(self.style.SUCCESS('Created Managers group with permissions'))

        # Users
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created superuser admin/admin123'))
        else:
            self.stdout.write('Superuser already exists')

        if not User.objects.filter(username='user').exists():
            User.objects.create_user('user', 'user@example.com', 'user123')
            self.stdout.write(self.style.SUCCESS('Created user user/user123'))
        else:
            self.stdout.write('User already exists')

        if not User.objects.filter(username='manager').exists():
            manager = User.objects.create_user('manager', 'manager@example.com', 'manager123')
            manager.groups.add(managers_group)
            ManagerProfile.objects.create(user=manager, is_manager=True)
            self.stdout.write(self.style.SUCCESS('Created manager user manager/manager123'))
        else:
            self.stdout.write('Manager user already exists')

        # Categories
        cats = [
            ('Живопись', 'painting'),
            ('Скульптура', 'sculpture'),
            ('Графика', 'graphics'),
        ]

        for name, slug in cats:
            Category.objects.get_or_create(slug=slug, defaults={'name': name})

        # Адреса магазинов (исправлены отступы)
        store_addresses = """Москва, ул. Тверская, д. 10
Санкт-Петербург, Невский пр., д. 25
Екатеринбург, ул. Ленина, д. 42
Новосибирск, Красный пр., д. 15
Казань, ул. Баумана, д. 7
Ростов-на-Дону, ул. Большая Садовая, д. 33
Владивосток, ул. Светланская, д. 18
Краснодар, ул. Красная, д. 22
Сочи, ул. Навагинская, д. 9
Калининград, пр. Мира, д. 12"""

        # Products
        painting = Category.objects.get(slug='painting')

        if Product.objects.count() < 5:
            for i in range(1, 6):
                # Добавляем уникальные описания для каждого товара
                descriptions = [
                    "Картина маслом на холсте. Современный абстрактный стиль.",
                    "Пейзаж с изображением морского побережья. Масляные краски.",
                    "Портрет в стиле импрессионизма. Холст, масло.",
                    "Абстрактная композиция с геометрическими формами.",
                    "Натюрморт с фруктами и цветами. Классическая техника."
                ]

                Product.objects.create(
                    category=painting,
                    name=f'Тестовая картина {i}',
                    slug=f'test-painting-{i}',
                    description=descriptions[i - 1],
                    price=1000 + i * 250,
                    store_addresses=store_addresses
                )
            self.stdout.write(self.style.SUCCESS('Created 5 demo products'))
        else:
            # Обновляем существующие товары, добавляя адреса магазинов
            for product in Product.objects.all():
                if not product.store_addresses:
                    product.store_addresses = store_addresses
                    product.save()
            self.stdout.write('Updated existing products with store addresses')

        self.stdout.write(self.style.SUCCESS('Seeding complete'))