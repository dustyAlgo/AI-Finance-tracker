from langchain.agents import create_agent
from langchain_core.language_models import LLM
from typing import Optional, List, Dict, Any, Sequence
from finance.services.summary_service import get_monthly_summary, get_category_spending
from django.contrib.auth import get_user_model
import json

from finance.ai.tools import (
    get_monthly_summary_tool,
    get_category_spending_tool,
)
from finance.ai.llm import call_llama

class LlamaLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "llama-hf"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {"name": "llama-hf"}

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        # Ensure string output always
        response = call_llama(prompt)
        return str(response)

    def bind_tools(self, tools: Sequence[Any], **kwargs: Any) -> "LlamaLLM":
        """Required for LangChain ≥1.0"""
        return self


def run_finance_agent(user_id: int, year: int, month: int) -> str:
    User = get_user_model()
       
    # 1. ACTUALLY CALL YOUR TOOLS
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return "User not found."
    
    summary = get_monthly_summary(user, year, month)
    categories = get_category_spending(user, year, month)
    
    # 2. LLM ANALYSIS ONLY (no tool hallucination possible)
    prompt = f"""
    Analyze this EXACT financial data for user_id={user_id}, {year}-{month:02d}:
    
    SUMMARY: {json.dumps(summary)}
    CATEGORIES: {json.dumps(categories)}
    Keep the response short and concise and the response should only contain natural language. 
    Generate insights using these data values only:
    - Income vs expenses ratio and keep all values in Indian Rupee
    - Food expense percentage in total expenses: Food expense > 25% expenses? → "High food spending" 
    - Rent expense percentage in total expenses: Rent > 40% expenses? → "High rent burden"
    - Travel expenses % in total expense: Travel > 10% expenses? → "Reduce travel"
    - Savings expense % in Total income: Savings < 20% income? → "Increase savings"
    If all zeros: "No transactions found for this period"
    
    """
    
    analysis = call_llama(prompt)
    return analysis
