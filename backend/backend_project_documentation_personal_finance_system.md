# Backend Project Documentation – Personal Finance System

## 1. Project Overview

This backend powers a **personal finance tracking and insight system**. It exposes secure APIs for:
- User authentication
- Tracking income and expenses
- Categorizing transactions
- Computing monthly summaries
- Providing structured data for analytics, ML models, and LLM-based insights

The backend is **API-only**, built with **Django + Django REST Framework**, and consumed by a **React frontend**.

---

## 2. Tech Stack

- **Language**: Python 3.x
- **Framework**: Django
- **API Layer**: Django REST Framework (DRF)
- **Authentication**: JWT (`djangorestframework-simplejwt`)
- **Database**: SQLite (dev) / PostgreSQL (recommended for prod)

---

## 3. High-Level Architecture

```
React Frontend
     |
     |  JWT (Bearer Token)
     v
Django REST API
     |
     ├── Auth (accounts app)
     ├── Finance Domain (finance app)
     │     ├── Category
     │     ├── Transaction
     │     └── MonthlySummary
     └── Analytics / ML / LLM (future)
```

The backend is **stateless**. All authentication is handled via JWT.

---

## 4. Apps Overview

### 4.1 `accounts` app
Responsible for:
- Custom user model
- User registration
- JWT-based login

### 4.2 `finance` app
Responsible for:
- Categories
- Transactions
- Monthly summaries
- Analytics-ready queries

---

## 5. Authentication Design

### User Model
- Custom user model extending `AbstractUser`
- Fields:
  - `username`
  - `email` (unique, used for login)
  - `password` (hashed by Django)

### Auth Flow
1. User registers
2. User logs in with email + password
3. Backend returns JWT access + refresh tokens
4. Frontend sends access token in `Authorization: Bearer <token>` header

### Logout
- Stateless
- Frontend deletes tokens

---

## 6. Database Models

### 6.1 Category
Represents user-defined spending or income categories.

**Fields**:
- `user` (FK → User)
- `name`

**Constraints**:
- Unique per user (`user + name`)

---

### 6.2 Transaction
Represents a single financial event.

**Fields**:
- `user` (FK → User)
- `category` (FK → Category)
- `type` (`INCOME` | `EXPENSE`)
- `amount` (Decimal)
- `date` (Date only)
- `note` (optional)
- `created_at`

**Rules**:
- One transaction belongs to exactly one user and one category
- Category deletion is blocked if transactions exist

---

### 6.3 MonthlySummary
Stores precomputed aggregates for fast access and analytics.

**Fields**:
- `user` (FK → User)
- `year`
- `month`
- `total_income`
- `total_expense`
- `savings`
- `created_at`, `updated_at`

**Constraints**:
- One row per `(user, year, month)`

**Note**: This is derived data and should not be user-editable.

---

## 7. API Endpoints

### Auth
- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/refresh/`

---

### Categories
- `GET /api/finance/categories/` – List user categories
- `POST /api/finance/categories/` – Create category

---

### Transactions
- `GET /api/finance/transactions/` – List user transactions
- `POST /api/finance/transactions/` – Create transaction
- `GET /api/finance/transactions/{id}/` – Retrieve transaction
- `PATCH /api/finance/transactions/{id}/` – Update transaction
- `DELETE /api/finance/transactions/{id}/` – Delete transaction

All endpoints require JWT authentication.

---

## 8. Core Backend Functions (Service-Level)

These functions represent **business logic** and are designed to later become **LangChain tools**.

### `get_transactions(user_id, date_range)`
Returns all transactions for a user within a date range.

### `get_category_breakdown(user_id, month)`
Returns total expense grouped by category for a given month.

### `get_income_vs_expense(user_id, month)`
Returns aggregated income vs expense for a month.

### `get_anomalies(user_id, month)`
Identifies unusual spending patterns by comparing with historical data.

---

## 9. Security & Data Isolation

- JWT required for all finance APIs
- Querysets always filtered by `request.user`
- No user ID is accepted from client input
- Cross-user access is impossible by design

---

## 10. Analytics & ML Readiness

- Clean relational schema
- Decimal-based financial values
- Category-based grouping
- MonthlySummary enables fast reads
- Minimal, structured outputs suitable for LLM prompts

---

## 11. Adding New Features (Guidelines)

When extending the system:

1. **Add logic in service layer**, not directly in views
2. Keep models normalized; derived data goes into `MonthlySummary`
3. Never trust client-sent user identifiers
4. Prefer aggregation queries over Python loops
5. Keep LLM-facing data small and structured

Examples of safe extensions:
- Budget limits per category
- Alerts and notifications
- Advanced anomaly detection (ML)
- Natural language financial summaries

---

## 12. Development Workflow

1. Update models (if needed)
2. Create migrations
3. Add serializers
4. Add views with auth protection
5. Test via Postman
6. Update this documentation

---

## 13. Environment Setup (Quick)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 14. Ownership & Maintenance

- Backend is modular and domain-driven
- New contributors should read:
  1. Models
  2. Service-level functions
  3. API views

This document should be updated whenever schema or responsibilities change.
