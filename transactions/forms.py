from django import forms
from django.forms import ModelForm
from .models import Transaction, Status, TransactionType, Category, Subcategory


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['created_at', 'status', 'transaction_type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'created_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control', 'id': 'id_transaction_type'}),
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'id_category'}),
            'subcategory': forms.Select(attrs={'class': 'form-control', 'id': 'id_subcategory'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Инициализируем пустые queryset для категорий и подкатегорий
        self.fields['category'].queryset = Category.objects.none()
        self.fields['subcategory'].queryset = Subcategory.objects.none()

        # Если есть данные (POST или instance), заполняем queryset
        if 'transaction_type' in self.data:
            try:
                transaction_type_id = int(self.data.get('transaction_type'))
                self.fields['category'].queryset = Category.objects.filter(transaction_type_id=transaction_type_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['category'].queryset = Category.objects.filter(transaction_type=self.instance.transaction_type)

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = Subcategory.objects.filter(category=self.instance.category)
