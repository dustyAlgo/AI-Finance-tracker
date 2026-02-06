from django.db.models import Sum
from django.db.models.functions import Coalesce
from finance.models import Transaction


def get_monthly_summary(user, year: int, month: int) -> dict:
    """
    Returns total income, expenses, and savings for a given month.
    """

    transactions = Transaction.objects.filter(
        user=user,
        date__year=year,
        date__month=month
    )
    income_result = transactions.filter(type="INCOME").aggregate(total=Sum("amount"))
    income = income_result["total"] or 0

    expenses_result = transactions.filter(type="EXPENSE").aggregate(total=Sum("amount"))
    expenses = expenses_result["total"] or 0
    

    

    savings = income - expenses

    return {
        "income": float(income),
        "expenses": float(expenses),
        "savings": float(savings)
    }


def get_category_spending(user, year: int, month: int) -> dict:
    """
    Returns category-wise expense totals for a given month.
    """

    transactions = (
        Transaction.objects
        .filter(
            user=user,
            type="EXPENSE",
            date__year=year,
            date__month=month
        )
        .values("category__name")
        .annotate(total=Sum("amount"))
    )

    result = {}
    for t in transactions:
        category = t["category__name"] or "Uncategorized"
        result[category] = float(t["total"])

    return result
