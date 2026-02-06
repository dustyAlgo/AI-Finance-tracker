# ML Integration Documentation

## Overview

This project integrates a Machine Learning pipeline into the transaction system to:

- Predict transaction categories from user notes
- Detect anomalous transactions using statistical methods
- Allow user override, where manual category selection always takes priority over ML prediction

The system is designed to be:
- Simple
- Interpretable
- Easy to extend
- Production-ready

## Core Concept

Each transaction stores two category fields:

| Field | Purpose |
|-------|---------|
| `category` | Final category (user-selected or ML-assigned) |
| `predicted_category` | Category suggested by ML model |

**Priority Rule:** User category > ML predicted category

- If the user selects a category: That becomes the final category
- If the user does not select a category: ML prediction is used

## System Architecture

```
User Input (note)
        ↓
ML Prediction API
        ↓
Predicted Category
        ↓
Transaction Creation
        ↓
Serializer Logic
        ↓
Final Category Assignment
```

## Database Schema

### Category Model
```
Category
---------
id
user (FK)
name
```

Each user has their own set of categories.

**Default categories:**
- Food
- Rent
- Travel
- Utilities
- Entertainment
- Healthcare
- Other

Transaction Model
Transaction
------------
id
user (FK)
type (INCOME / EXPENSE)
amount
date
note
category (FK)              ← final category
predicted_category (FK)    ← ML suggestion
anomaly_z_score (float)

ML Components

The ML system performs two tasks:

1. Category Prediction

Goal: Predict transaction category from the text note.

Example:

Input:  "uber to airport"
Output: Travel

Model

Text Vectorizer: TF-IDF

Classifier: Multinomial Naive Bayes (or similar)

Training Data

Transactions with:

note + category

2. Anomaly Detection

Goal: Detect unusual transaction amounts.

Method

Z-score calculation:

z = (amount − mean) / standard deviation


If:

|z| > threshold


→ Transaction is marked as anomalous.

Stored in:

anomaly_z_score

API Endpoints
1. Predict Category

Endpoint

POST /api/finance/transactions/predict-category/


Request

{
  "note": "uber ride"
}


Response

{
  "predicted_category": "travel"
}

2. List Categories

Endpoint

GET /api/finance/categories/


Response

[
  { "id": 13, "name": "Food" },
  { "id": 14, "name": "Rent" },
  { "id": 15, "name": "Travel" }
]

3. Create Transaction

Endpoint

POST /api/finance/transactions/


Example Request (with user category)

{
  "type": "EXPENSE",
  "amount": 2000,
  "date": "2026-01-20",
  "note": "rent payment",
  "category": 14
}


Behavior

User selected category → final category = Rent

ML prediction ignored

Example Request (without category)

{
  "type": "EXPENSE",
  "amount": 500,
  "date": "2026-01-20",
  "note": "pizza"
}


Behavior

ML predicts: Food

Final category = Food

Serializer Logic (Final Category Assignment)
Business Rule
if category provided by user:
    keep category
else if predicted_category exists:
    set category = predicted_category


This ensures:

User always has control

ML only assists, never overrides

Data Ingestion (Synthetic Data)

Synthetic data is used to:

Train the ML model

Simulate real user behavior

Script Behavior

For each user:

Create default categories

Generate transactions

Assign:

Realistic notes

Correct category labels

Leave:

predicted_category = NULL

anomaly_z_score = NULL

Training Pipeline
Step-by-Step

Fetch transactions:

SELECT note, category FROM transactions
WHERE category IS NOT NULL


Clean text:

Lowercase

Remove punctuation

Vectorize notes:

TF-IDF Vectorizer


Train classifier:

Multinomial Naive Bayes


Save model:

model.pkl
vectorizer.pkl

Prediction Flow

When user sends a note:

1. Receive note
2. Clean text
3. Vectorize
4. Predict category
5. Match predicted name with user's categories
6. Return category ID

Important Design Decisions
1. User-specific categories

Each user has their own category IDs.

Reason:

Multi-tenant architecture

User customization

2. Case-insensitive matching

Prediction uses:

lowercase(category_name)


Prevents mismatch:

"Travel" vs "travel"

3. User override priority

User selection is always final.

Reason:

Improves trust in system

Prevents incorrect automation