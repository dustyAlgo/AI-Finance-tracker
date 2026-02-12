from rest_framework import generics, permissions
from .models import Transaction
from .serializers import TransactionSerializer
from .models import Category
from .serializers import CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .ml.inference import predict_category
from finance.ml.anomaly_service import compute_z_score
from .serializers import MonthlyAISummaryRequestSerializer
from finance.ai.agent import run_finance_agent
from rest_framework.permissions import IsAuthenticated
from finance.services.summary_service import (
    get_monthly_summary,
    get_category_spending,
)



class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        transaction = serializer.save(user=self.request.user)

        # Only run for EXPENSE
        if transaction.type == "EXPENSE":

    # User category has highest priority
            final_category_id = (
                transaction.category_id
                if transaction.category_id
                else transaction.predicted_category_id
            )

            if final_category_id:
                z_score = compute_z_score(
                    user_id=transaction.user_id,
                    category_id=final_category_id,
                    amount=transaction.amount
                )

                if z_score is not None:
                    transaction.anomaly_z_score = z_score
                    transaction.save(update_fields=["anomaly_z_score"])



class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PredictCategoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        note = request.data.get('note', '').strip()

        if not note:
            return Response(
                {"detail": "Note is required for prediction."},
                status=status.HTTP_400_BAD_REQUEST
            )

        predicted_category_id = predict_category(note)

        return Response(
            {"predicted_category": predicted_category_id},
            status=status.HTTP_200_OK
)

class MonthlyAISummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MonthlyAISummaryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        year = serializer.validated_data["year"]
        month = serializer.validated_data["month"]
        user_id = request.user.id

        try:
            summary = run_finance_agent(
                user_id=user_id,
                year=year,
                month=month
            )
            return Response({"summary": summary})

        except Exception:
            return Response(
                {"error": "AI service unavailable"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class MonthlySummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = request.query_params.get("year")
        month = request.query_params.get("month")
        try:
            year = int(year)
            month = int(month)
            if not (1 <= month <= 12):
                raise ValueError
        except Exception:
            return Response(
                {"detail": "Query params `year` and `month` (1-12) are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        summary = get_monthly_summary(user=request.user, year=year, month=month)
        return Response({"summary": summary}, status=status.HTTP_200_OK)


class CategoryBreakdownAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = request.query_params.get("year")
        month = request.query_params.get("month")
        try:
            year = int(year)
            month = int(month)
            if not (1 <= month <= 12):
                raise ValueError
        except Exception:
            return Response(
                {"detail": "Query params `year` and `month` (1-12) are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        breakdown = get_category_spending(user=request.user, year=year, month=month)
        return Response({"breakdown": breakdown}, status=status.HTTP_200_OK)