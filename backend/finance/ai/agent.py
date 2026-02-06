from langchain.agents import create_agent
from langchain_core.language_models import LLM
from typing import Optional, List
from finance.ai.tools import (
    get_monthly_summary_tool,
    get_category_spending_tool,
)
from finance.ai.llm import call_llama

class LlamaLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "llama-hf"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        return call_llama(prompt)

def run_finance_agent(user_id: int, year: int, month: int) -> str:
    """
    Runs the finance AI agent and returns a natural language summary.
    """

    llm = LlamaLLM()

    tools = [
        get_monthly_summary_tool,
        get_category_spending_tool,
    ]

    system_prompt = (
        "You are a personal financial analyst.\n"
        "You must use tools to retrieve accurate data.\n"
        "Never guess numbers.\n"
        "And if the data is insufficient then explicitly tell the User.\n"
        "Base suggestions strictly on retrieved data.\n"
        "Provide a short summary and 3 improvement suggestions."
    )

    agent_graph = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )

    query = (
        f"Generate a financial summary for user_id={user_id} "
        f"for year={year} and month={month}."
    )

    # Use the graph with an input state
    result = agent_graph.invoke({
        "messages": [{"role": "user", "content": query}]
    })

    # Extract the final response from the graph output
    return result["messages"][-1]["content"]