# ShopList - Интернет-магазин картин
<img width="1920" height="1044" alt="Главная страница" src="https://github.com/user-attachments/assets/f8bbc4c5-3067-4b2f-a034-7b0f2f6546bf" />

![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10-blue.svg)

Современный интернет-магазин картин с адаптивным дизайном, корзиной покупок и системой управления заказами.

## ✨ Особенности

- 🎨 **Каталог товаров** с фильтрацией по категориям
- 🛒 **Корзина покупок** с сессионным хранением
- 👤 **Система аутентификации** с регистрацией и личным кабинетом
- 📱 **Адаптивный дизайн** для мобильных и десктопных устройств
- ⚡ **Быстрый интерфейс** на основе Tailwind CSS
- 🗺️ **Интеграция с Яндекс.Картами** для отображения магазинов
- 👔 **Панель управления** для менеджеров и администраторов
- 💳 **Готовность к интеграции** с платежными системами (ЮKassa)

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.10+
- pip (менеджер пакетов Python)
- Виртуальное окружение (рекомендуется)

### Установка

1. Клонируйте репозиторий:
```bash
git clone <ссылка-на-репозиторий>
cd shoplist
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Примените миграции:
```bash
python manage.py migrate
```

5. Загрузите тестовые данные:
```bash
python manage.py seed_data
```

6. Запустите сервер разработки:
```bash
python manage.py runserver
```

7. Откройте в браузере: http://localhost:8000

## 👤 Тестовые аккаунты

После выполнения команды `seed_data` создаются тестовые пользователи:

- **Администратор**: login: `admin`, password: `admin123`
- **Менеджер**: login: `manager`, password: `manager123` (создайте через админку)
- **Пользователь**: login: `user`, password: `user123`

## 📁 Структура проекта

```
shoplist/
├── ShopList/                 # Настройки проекта
├── cart/                     # Приложение корзины и заказов
├── shop/                     # Приложение каталога товаров
├── users/                    # Приложение пользователей
├── pages/                    # Статические страницы
├── manager/                  # Панель управления для менеджеров
├── templates/                # HTML шаблоны
│   ├── base.html            # Базовый шаблон
│   ├── shop/                # Шаблоны каталога
│   ├── cart/                # Шаблоны корзины
│   ├── users/               # Шаблоны пользователей
│   ├── pages/               # Статические страницы
│   └── manager/             # Панель управления
├── static/                   # Статические файлы
│   ├── css/                 # Кастомные стили
│   ├── images/              # Изображения (лого, placeholder)
│   └── js/                  # JavaScript файлы
├── media/                    # Загружаемые файлы (изображения товаров)
├── requirements.txt          # Зависимости проекта
└── manage.py                # Утилита управления Django
```

## 🛠️ Функциональность

### Для пользователей
- Регистрация и авторизация
- Просмотр каталога товаров
- Фильтрация товаров по категориям
- Добавление товаров в корзину
- Оформление заказов
- Просмотр истории заказов
- Личный кабинет

### Для менеджеров
- Просмотр всех заказов
- Изменение статусов заказов
- Просмотр деталей заказов
- Управление товарами (активация/деактивация)
- Экспорт данных в CSV

### Для администраторов
- Полный доступ через Django Admin
- Управление пользователями и правами
- Управление товарами и категориями
- Просмотр аналитики продаж

## 🌐 Деплой

### На PythonAnywhere

1. Создайте аккаунт на [PythonAnywhere](https://www.pythonanywhere.com/)
2. Создайте веб-приложение с ручной конфигурацией
3. Настройте виртуальное окружение
4. Загрузите код через Git или загрузку файлов
5. Настройте базу данных MySQL
6. Обновите настройки в `settings.py` для продакшена
7. Выполните миграции и соберите статические файлы

### Настройка домена и SSL

1. Зарегистрируйте домен у любого регистратора
2. Настройте DNS-записи для вашего домена
3. В панели PythonAnywhere настройте домен и SSL
4. Обновите `ALLOWED_HOSTS` в настройках Django

## 🔧 Настройки

Основные настройки находятся в `ShopList/settings.py`:

```python
# Базовые настройки
DEBUG = True  # Для разработки, для продакшена установите False
ALLOWED_HOSTS = ['yourdomain.com', 'localhost']

# База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Для разработки
        # Для продакшена используйте MySQL или PostgreSQL
    }
}

# Статические файлы
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Настройки интернационализации
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
```

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие проекта! Для этого:

1. Форкните репозиторий
2. Создайте ветку для вашей функции (`git checkout -b feature/amazing-feature`)
3. Закоммитьте изменения (`git commit -m 'Add some amazing feature'`)
4. Запушьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробнее см. в файле `LICENSE`.

## 📞 Поддержка

Если у вас возникли вопросы или проблемы:

1. Проверьте логи приложения для детальной информации об ошибках
2. Убедитесь, что все миграции применены
3. Проверьте настройки базы данных и переменные окружения
4. Создайте issue в репозитории проекта

## 🚀 Дальнейшее развитие

Планируемые улучшения:
- Интеграция с платежными системами (ЮKassa, Stripe)
- Email-уведомления о заказах
- Система отзывов и рейтингов товаров
- Избранные товары
- Промокоды и система скидок
- REST API для мобильного приложения

<img width="1920" height="798" alt="Каталог" src="https://github.com/user-attachments/assets/004908ca-b50a-4093-80a7-156cdcb01b4d" />
<img width="1920" height="1032" alt="Лист товара" src="https://github.com/user-attachments/assets/fb2fe26a-cfd5-4989-805d-16aacd6a78e4" />
<img width="1920" height="1042" alt="Панель управления менеджера (только для менеджеров)" src="https://github.com/user-attachments/assets/93ddebc6-29c4-418e-a8f6-ba3145019a38" />
<img width="1916" height="1042" alt="Админ панель" src="https://github.com/user-attachments/assets/76d1ac7b-12ef-4797-a015-0de9539fc12b" />
<img width="1918" height="1040" alt="Товарный лист" src="https://github.com/user-attachments/assets/e042345c-b72c-459d-a85c-cdbc6aafd6db" />
<img width="1920" height="628" alt="Мои заказы" src="https://github.com/user-attachments/assets/84f787a1-ec67-4d06-948c-ccda6254e015" />
<img width="1920" height="400" alt="Корзина" src="https://github.com/user-attachments/assets/057a8e42-5ac4-4c01-b0bd-c01667521c29" />
<img width="1450" height="598" alt="Оформление заказа" src="https://github.com/user-attachments/assets/4a97685c-2e00-4e66-abc5-6ea2b2894c46" />
<img width="1920" height="1040" alt="Вход" src="https://github.com/user-attachments/assets/115564fa-5560-487d-b8be-7f44a5f515d8" />



**Примечание**: Для работы в продакшене обязательно настройте безопасные SECRET_KEY, пароли БД и ключи API в переменных окружения, а не в коде.
