from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils import timezone
from .models import Transaction, Status, TransactionType, Category, Subcategory
from .forms import TransactionForm


class TransactionListView(ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        queryset = Transaction.objects.all()

        # Фильтрация по дате
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        # Фильтрация по статусу
        status_id = self.request.GET.get('status')
        if status_id:
            queryset = queryset.filter(status_id=status_id)

        # Фильтрация по типу
        transaction_type_id = self.request.GET.get('transaction_type')
        if transaction_type_id:
            queryset = queryset.filter(transaction_type_id=transaction_type_id)

        # Фильтрация по категории
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Фильтрация по подкатегории
        subcategory_id = self.request.GET.get('subcategory')
        if subcategory_id:
            queryset = queryset.filter(subcategory_id=subcategory_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['types'] = TransactionType.objects.all()
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        return context


class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transaction_list')

    def get_initial(self):
        initial = super().get_initial()
        initial['created_at'] = timezone.now().date()
        return initial


class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transaction_list')


class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction_list')


def get_categories(request, transaction_type_id):
    categories = Category.objects.filter(transaction_type_id=transaction_type_id).values('id', 'name')
    return JsonResponse({'categories': list(categories)})


def get_subcategories(request, category_id):
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse({'subcategories': list(subcategories)})


def reference_manage(request):
    context = {
        'statuses': Status.objects.all(),
        'types': TransactionType.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
    }
    return render(request, 'transactions/reference_manage.html', context)
