from langchain_core.tools import tool
from finance.services.summary_service import (
    get_monthly_summary,
    get_category_spending,
)


@tool
def get_monthly_summary_tool(user_id: int, year: int, month: int) -> dict:
    """
    Returns total income, expenses, and savings for a given user and month.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    user = User.objects.get(id=user_id)
    
    return get_monthly_summary(
        user=user,
        year=year,
        month=month
    )


@tool
def get_category_spending_tool(user_id: int, year: int, month: int) -> dict:
    """
    Returns category-wise expense totals for a given user and month.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    user = User.objects.get(id=user_id)
    
    return get_category_spending(
        user=user,
        year=year,
        month=month
    )
