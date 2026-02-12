# AI Finance Tracker - Backend

## Project Overview
AI Finance Tracker is a comprehensive personal finance management system built with Django and Azure cloud services. It features intelligent expense anomaly detection using machine learning, transaction categorization, and real-time financial insights.

## Directory Structure & Technology Stack

### Root Level
- `manage.py` - Django management script
- `db.sqlite3` - Local SQLite database
- `Readme.md` - Project documentation

### `accounts/` - User Authentication & Profiles
**Tech Stack:** Django, Django REST Framework
- User registration and authentication
- User profile management
- Serializers for API endpoints
- Models for account data
- Unit tests for account functionality

### `backend/` - Django Core Configuration
**Tech Stack:** Django
- `settings.py` - Django configuration (database, installed apps, middleware)
- `urls.py` - Root URL routing
- `wsgi.py` - WSGI application entry point
- `asgi.py` - ASGI application entry point

### `finance/` - Main Finance Application
**Tech Stack:** Django, Django REST Framework, Machine Learning
- **Core files:**
  - `models.py` - Transaction, Category, MonthlySummary models
  - `serializers.py` - API serializers for finance endpoints
  - `views.py` - REST API endpoints for transactions and analytics
  - `urls.py` - Finance app URL routing
  - `admin.py` - Django admin configuration

- **`ai/` - AI Agent & LLM Integration**
  - `agent.py` - AI agent orchestration
  - `llm.py` - Language model integration
  - `tools.py` - AI tools and utilities
  - `testllm.py` - LLM testing utilities

- **`ml/` - Machine Learning Services**
  - `anomaly_service.py` - Anomaly detection service
  - `anomaly.py` - Anomaly detection algorithms
  - `inference.py` - ML model inference
  - `predict.py` - Transaction predictions
  - `models/` - Trained ML models storage

- **`services/` - Business Logic**
  - `summary_service.py` - Transaction summary calculations

- **`management/commands/` - Django Custom Commands**
  - `train_expense_classifier.py` - Train ML classifier
  - `compute_anomaly_stats.py` - Compute statistical anomaly metrics
  - `migrate_anomaly_stats.py` - Migrate anomaly statistics

### `financetrack_function/` - Azure Functions
**Tech Stack:** Python, Azure Functions, Azure Storage, Azure SQL, pyodbc
- `function_app.py` - Azure Function app with HTTP triggers
- `requirements.txt` - Python dependencies (azure-functions, azure-storage-queue, pyodbc)
- `host.json` - Azure Functions runtime configuration
- `local.settings.json` - Local development settings
- **Functions:**
  - `score_transaction` - HTTP endpoint for real-time transaction anomaly scoring

## Tech Stack Summary

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Django 4.x, Django REST Framework |
| **Database** | SQLite (local), Azure SQL (production) |
| **API** | REST API via DRF |
| **ML/AI** | Python ML libraries, LLM integration |
| **Cloud** | Azure Functions, Azure Storage, Azure SQL |
| **ML Model** | Scikit-learn (anomaly detection, classification) |

## Key Features
- 🔐 User authentication and account management
- 💹 Transaction tracking and categorization
- 🤖 ML-based expense anomaly detection
- 📊 Monthly financial summaries
- 🔍 AI-powered financial insights
- ☁️ Serverless transaction scoring via Azure Functions