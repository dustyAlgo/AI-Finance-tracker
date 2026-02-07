from langchain.agents import create_agent
from langchain_core.language_models import LLM
from typing import Optional, List, Dict, Any, Sequence

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
    """
    Runs the finance AI agent using LangChain 1.2.9 create_agent API.
    """

    llm = LlamaLLM()

    tools = [
        get_monthly_summary_tool,
        get_category_spending_tool,
    ]

    agent_graph = create_agent(
        model=llm,
        tools=tools,
        system_prompt=(
             """You are a PERSONAL FINANCIAL ANALYST for Indian users. 

                ## STRICT RULES:
                1. You HAVE financial data via TOOLS - NEVER ask for user data
                2. ONLY use data from get_monthly_summary_tool and get_category_spending_tool
                3. NEVER mention external sources (BLS/FRED/IRS) - you have NO internet
                4. Indian rupees (₹) ONLY - no USD conversion
                5. If tools return empty data: "No transactions found for this period"

                ## REAct FORMAT - YOU MUST FOLLOW:
                Thought: Analyze what tools to call
                Action: get_monthly_summary_tool OR get_category_spending_tool
                Action Input: {"user_id": 53, "year": 2025, "month": 2}

                ## INSIGHTS TO GIVE (SIMPLE):
                - Income vs expenses ratio
                - Food > 25% expenses? → "High food spending"
                - Rent > 40% expenses? → "High rent burden" 
                - Travel > 10% expenses? → "Reduce travel"
                - Savings < 20% income? → "Increase savings"

                ## SAMPLE OUTPUT FORMAT:
                **Feb 2025 Summary**
                Income: ₹80,000 | Expenses: ₹65,000 | Savings: ₹15,000 (19%)

                **Category Analysis:**
                - Food: ₹18,000 (28%) ← HIGH - cut dining out
                - Rent: ₹25,000 (38%) ← HIGH - negotiate lease
                - Travel: ₹12,000 (18%) ← HIGH - use public transport

                **3 Actionable Tips:**
                1. Reduce food spending by ₹5,000/month
                2. Cook at home 4 days/week  
                3. Cancel unused subscriptions"""
        ),
    )

    query = (
        f"Generate financial summary for user_id={user_id}, "
        f"year={year}, month={month}. "
        f"Include summary and 3 actionable suggestions."
    )

    result = agent_graph.invoke({
        "input": query
    })

    # Safely extract final message
    messages = result.get("messages", [])
    if not messages:
        return "No response generated."

    return messages[-1].content
