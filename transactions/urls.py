from django.urls import path
from . import views


urlpatterns = [
    path('', views.TransactionListView.as_view(), name='transaction_list'),
    path('create/', views.TransactionCreateView.as_view(), name='transaction_create'),
    path('update/<int:pk>/', views.TransactionUpdateView.as_view(), name='transaction_update'),
    path('delete/<int:pk>/', views.TransactionDeleteView.as_view(), name='transaction_delete'),
    path('get-categories/<int:transaction_type_id>/', views.get_categories, name='get_categories'),
    path('get-subcategories/<int:category_id>/', views.get_subcategories, name='get_subcategories'),
    path('references/', views.reference_manage, name='reference_manage'),
]
