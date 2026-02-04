from django.urls import path
from .views import (
    CategoryListCreateView,
    TransactionListCreateView,
    TransactionDetailView,
    PredictCategoryView,   # NEW
)


urlpatterns = [
    path('categories/', CategoryListCreateView.as_view()),
    path('transactions/', TransactionListCreateView.as_view()),
    path('transactions/<int:pk>/', TransactionDetailView.as_view()),
    path('transactions/predict-category/', PredictCategoryView.as_view()),
]
