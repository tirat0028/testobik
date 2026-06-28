import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dds_project.settings')
django.setup()

from transactions.models import Status, TransactionType, Category, Subcategory


def init_data():
    # Создаем статусы
    statuses = ['Бизнес', 'Личное', 'Налог']
    for status_name in statuses:
        Status.objects.get_or_create(name=status_name)

    # Создаем типы транзакций
    types = ['Пополнение', 'Списание']
    for type_name in types:
        TransactionType.objects.get_or_create(name=type_name)

    # Создаем категории и подкатегории
    type_income = TransactionType.objects.get(name='Пополнение')
    type_expense = TransactionType.objects.get(name='Списание')

    # Категории для списания
    cat_infra, _ = Category.objects.get_or_create(name='Инфраструктура', transaction_type=type_expense)
    Subcategory.objects.get_or_create(name='VPS', category=cat_infra)
    Subcategory.objects.get_or_create(name='Proxy', category=cat_infra)

    cat_marketing, _ = Category.objects.get_or_create(name='Маркетинг', transaction_type=type_expense)
    Subcategory.objects.get_or_create(name='Farpost', category=cat_marketing)
    Subcategory.objects.get_or_create(name='Avito', category=cat_marketing)

    # Категории для пополнения
    cat_sales, _ = Category.objects.get_or_create(name='Продажи', transaction_type=type_income)
    Subcategory.objects.get_or_create(name='Товары', category=cat_sales)
    Subcategory.objects.get_or_create(name='Услуги', category=cat_sales)

    print("Начальные данные успешно добавлены!")


if __name__ == '__main__':
    init_data()
