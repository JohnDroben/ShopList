from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Category, Product


class Command(BaseCommand):
    help = 'Create demo categories, products and test users'

    def handle(self, *args, **options):
        # Users
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created superuser admin/admin123'))
        else:
            self.stdout.write('Superuser already exists')

        if not User.objects.filter(username='user').exists():
            User.objects.create_user('user', 'user@example.com', 'user123')
            self.stdout.write(self.style.SUCCESS('Created user user/user123'))
        else:
            self.stdout.write('User already exists')

        # Categories
        cats = [
            ('Живопись', 'painting'),
            ('Скульптура', 'sculpture'),
            ('Графика', 'graphics'),
        ]

        for name, slug in cats:
            Category.objects.get_or_create(slug=slug, defaults={'name': name})

        # Products
        import random
        painting = Category.objects.get(slug='painting')

        if Product.objects.count() < 5:
            for i in range(1, 6):
                Product.objects.create(
                    category=painting,
                    name=f'Тестовая картина {i}',
                    slug=f'test-painting-{i}',
                    description='Описание тестовой картины. Современный стиль, холст, масло.',
                    price=1000 + i * 250,
                )
            self.stdout.write(self.style.SUCCESS('Created 5 demo products'))
        else:
            self.stdout.write('Products already exist')

        self.stdout.write(self.style.SUCCESS('Seeding complete'))