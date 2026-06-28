from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.name


class TransactionType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Тип транзакции'
        verbose_name_plural = 'Типы транзакций'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE, related_name='categories', verbose_name='Тип транзакции')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} ({self.transaction_type})'


class Subcategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name='Категория')

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        unique_together = ('name', 'category')

    def __str__(self):
        return f'{self.name} ({self.category})'


class Transaction(models.Model):
    created_at = models.DateField(verbose_name='Дата создания')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='transactions', verbose_name='Статус')
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE, related_name='transactions', verbose_name='Тип')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='transactions', verbose_name='Категория')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='transactions', verbose_name='Подкатегория')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.amount} - {self.subcategory} ({self.created_at})'
