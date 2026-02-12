from django.urls import path
from .views import (
    CategoryListCreateView,
    TransactionListCreateView,
    TransactionDetailView,
    PredictCategoryView,
    MonthlyAISummaryView,
    CategoryBreakdownAPIView,
    MonthlySummaryAPIView,   # NEW
)


urlpatterns = [
    path('categories/', CategoryListCreateView.as_view()),
    path('transactions/', TransactionListCreateView.as_view()),
    path('transactions/<int:pk>/', TransactionDetailView.as_view()),
    path('transactions/predict-category/', PredictCategoryView.as_view()),
    path("ai/monthly-summary/", MonthlyAISummaryView.as_view()),
    path("monthly-summary/", MonthlySummaryAPIView.as_view()),
    path("category-breakdown/", CategoryBreakdownAPIView.as_view()),

]
