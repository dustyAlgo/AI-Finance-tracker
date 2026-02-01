SuperUser Email: test@email.com Username: Test, Password: Test123
New User:
    "username": "newuser",
    "email": "newuser@email.com",
    "password": "newuser123"
🧠 BACKEND (Django + DRF + LangChain)
backend/
│
├── manage.py
├── requirements.txt
├── .env
│
├── config/                    # Django project config
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── settings.py
│   ├── urls.py
│   └── celery.py              # optional (async tasks)
│
├── apps/
│   ├── users/                 # Auth & profiles
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── permissions.py
│   │
│   ├── transactions/          # Core finance data
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── services.py        # business logic
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── analytics/             # Deterministic finance logic
│   │   ├── services.py        # totals, breakdowns, trends
│   │   ├── anomalies.py       # anomaly detection
│   │   └── schemas.py
│   │
│   ├── ai/                    # ⭐ LangChain lives here
│   │   ├── llm.py             # Ollama LLM config
│   │   ├── prompts.py         # system + tool prompts
│   │   ├── tools.py           # LangChain tools
│   │   ├── agent.py           # Agent definition
│   │   ├── memory.py          # Conversation memory
│   │   └── schemas.py         # tool input/output models
│   │
│   ├── chat/                  # Chat API
│   │   ├── serializers.py
│   │   ├── views.py           # /chat endpoint
│   │   └── urls.py
│   │
│   └── common/
│       ├── exceptions.py
│       ├── utils.py
│       └── constants.py
│
└── tests/
    ├── test_transactions.py
    ├── test_analytics.py
    └── test_agent.py


🤖 FRONTEND (React)
frontend/
│
├── package.json
├── vite.config.js   (or CRA)
├── .env
│
├── public/
│
└── src/
    ├── main.jsx
    ├── App.jsx
    │
    ├── api/                     # Backend communication
    │   ├── axios.js
    │   ├── auth.js
    │   ├── transactions.js
    │   └── chat.js
    │
    ├── pages/
    │   ├── Login.jsx
    │   ├── Register.jsx
    │   ├── Dashboard.jsx
    │   └── Chat.jsx
    │
    ├── components/
    │   ├── chat/
    │   │   ├── ChatWindow.jsx
    │   │   ├── Message.jsx
    │   │   ├── ChatInput.jsx
    │   │   └── TypingIndicator.jsx
    │   │
    │   ├── charts/
    │   │   ├── SpendingChart.jsx
    │   │   └── TrendChart.jsx
    │   │
    │   └── common/
    │       ├── Button.jsx
    │       ├── Loader.jsx
    │       └── Modal.jsx
    │
    ├── context/
    │   ├── AuthContext.jsx
    │   └── ChatContext.jsx
    │
    ├── hooks/
    │   ├── useAuth.js
    │   └── useChat.js
    │
    ├── styles/
    │   └── main.css
    │
    └── utils/
        ├── formatCurrency.js
        └── dateHelpers.js