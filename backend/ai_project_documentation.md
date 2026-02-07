Below is a **precise, implementation-accurate documentation** for the **LLM + LangChain integration** in your personal finance system, based strictly on the details you confirmed.
No assumptions have been added.

---

# AI Integration Documentation

## Personal Finance Tracker – LLM + LangChain Module

---

# 1. Overview

This module adds an **AI-powered financial analyst** to the personal finance application.

The AI system:

* Retrieves financial data using backend tools
* Uses an LLM to reason over the data
* Generates:

  * Monthly financial summaries
  * Spending insights
  * Actionable improvement suggestions

The system follows a **tool-using agent architecture** to prevent hallucination and ensure all outputs are based on real data.

---

# 2. High-Level Architecture

```
Client (React / Postman)
        |
        v
Django REST API
        |
        |-- JWT Authentication
        |
        |-- MonthlyAISummaryView
                |
                v
        LangChain Agent
                |
        -------------------
        |                 |
        v                 v
Summary Tools       Hugging Face LLM
(Python services)   (Llama-3.1-8B)
        |
        v
PostgreSQL / SQLite
```

---

# 3. Technology Stack

| Component        | Technology                                |
| ---------------- | ----------------------------------------- |
| Backend          | Django + Django REST Framework            |
| Auth             | JWT (SimpleJWT)                           |
| Agent Framework  | LangChain 1.2.9                           |
| LLM Provider     | Hugging Face Inference Router             |
| Model            | `meta-llama/Llama-3.1-8B-Instruct:novita` |
| AI Communication | OpenAI-compatible HF router API           |
| Data Source      | SQLite (local dev)                        |

---

# 4. Directory Structure

Relevant AI-related structure:

```
finance/
├── ai/
│   ├── agent.py
│   ├── llm.py
│   └── tools.py
│
├── services/
│   └── summary_service.py
│
├── views.py
├── serializers.py
└── urls.py
```

---

# 5. AI System Design

## 5.1 Agent Philosophy

The agent is designed with strict rules:

* Never guess financial numbers
* Always retrieve data via tools
* Perform reasoning only after tool outputs
* Provide only data-backed suggestions

System role:

> “You are a personal financial analyst.
> You must use tools to retrieve accurate data.
> Never guess numbers.”

---

## 5.2 Tools Used by the Agent

Only **two tools** are currently implemented.

### 1. `get_monthly_summary_tool`

**Purpose:**
Returns total income, expenses, and savings for a month.

**Backed by:**

```
finance/services/summary_service.py
```

**Returns:**

```json
{
  "income": 80000,
  "expenses": 65000,
  "savings": 15000,
  "savings_rate": 19
}
```

---

### 2. `get_category_spending_tool`

**Purpose:**
Returns category-wise expense breakdown.

**Returns:**

```json
{
  "Food": 18000,
  "Rent": 25000,
  "Travel": 12000
}
```

---

## 5.3 Agent Workflow

1. API request arrives
2. Django view extracts:

   * `user_id` from JWT
   * `year`, `month` from request
3. View calls:

```
run_finance_agent(user_id, year, month)
```

4. Agent:

   * Calls summary tool
   * Calls category tool
   * Sends tool data to LLM
5. LLM produces:

   * Summary
   * Insights
   * 3 suggestions
6. Output is cleaned
7. Response returned to client

---

# 6. LLM Integration

## 6.1 File

```
finance/ai/llm.py
```

## 6.2 LLM Provider

Hugging Face Inference Router using OpenAI-compatible API.

### Model

```
meta-llama/Llama-3.1-8B-Instruct:novita
```

---

## 6.3 API Setup

Environment variable required:

```
HF_TOKEN=<your_huggingface_api_key>
```

---

## 6.4 LLM Call Logic

The system uses a helper function:

```python
call_llama(prompt: str) -> str
```

Responsibilities:

* Send prompt to HF router
* Receive model output
* Return plain text response

---

# 7. LangChain Agent Implementation

## File

```
finance/ai/agent.py
```

---

## 7.1 Custom LLM Wrapper

LangChain 1.2.9 requires:

* `LLM` subclass
* `bind_tools()` method

Implemented as:

```python
class LlamaLLM(LLM):
    def _call(self, prompt, stop=None):
        return call_llama(prompt)

    def bind_tools(self, tools, **kwargs):
        return self
```

---

## 7.2 Agent Creation

Agent is created using the new LangChain 1.x API:

```python
agent_graph = create_agent(
    model=llm,
    tools=tools,
    system_prompt="..."
)
```

---

## 7.3 Agent Execution

```python
result = agent_graph.invoke({
    "input": query
})
```

---

## 7.4 Output Cleaning

Since the agent uses ReAct reasoning, output contains:

* Thoughts
* Tool calls
* Final answer

These are removed using a post-processing step:

```python
raw_output = messages[-1].content
# trim reasoning traces
return clean_output.strip()
```

---

# 8. AI API Endpoint

## Endpoint

```
POST /api/finance/ai/monthly-summary/
```

---

## Authentication

* JWT required
* User determined from token
* No user_id accepted from client

---

## Request Body

```json
{
  "year": 2025,
  "month": 2
}
```

---

## Response (Success)

```json
{
  "summary": "AI generated financial summary..."
}
```

---

## Response (Error)

```json
{
  "error": "AI service unavailable"
}
```

HTTP status:

```
500 Internal Server Error
```

---

# 9. View Implementation

File:

```
finance/views.py
```

Core logic:

```python
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
```

---

# 10. Security Considerations

| Area                     | Implementation           |
| ------------------------ | ------------------------ |
| Authentication           | JWT required             |
| Multi-user isolation     | user_id from token       |
| Data leakage             | Tools scoped to user_id  |
| Hallucination prevention | Tool-only reasoning rule |

---

# 11. Current Limitations

1. Only monthly summaries supported
2. Only two tools available
3. No caching of AI responses
4. No rate limiting
5. Plain text output only
6. No async processing (blocking API call)

---

# 12. Possible Future Enhancements

## New Tools

* `get_anomalies`
* `compare_months`
* `get_savings_rate`
* `forecast_cashflow`

## System Improvements

* AI response caching
* Background job queue (Celery)
* Structured JSON output
* Natural language query endpoint

---

# 13. End-to-End Flow Summary

1. Client sends:

```
POST /api/finance/ai/monthly-summary/
```

2. JWT authenticated
3. Django extracts user_id
4. Agent runs tools
5. LLM generates insights
6. Output cleaned
7. Response returned

---
