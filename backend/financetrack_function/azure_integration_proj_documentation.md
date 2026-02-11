
# Finance Tracker – Azure Anomaly Detection Integration

---

## 1. Project Overview

This project extends a **Django-based personal finance tracking application** with a **serverless anomaly detection pipeline** using Microsoft Azure free-tier services.

The goal is to:

* Detect unusual financial transactions using statistical methods.
* Process anomalies in real time.
* Store results in a cloud database.
* Trigger automated email alerts.

This integration demonstrates:

* Cloud-native event-driven architecture
* Serverless compute
* Managed SQL database usage
* Queue-based decoupling
* Automated workflow orchestration

---

## 2. High-Level Architecture

### End-to-End Flow

```
Django Backend
      │
      │ HTTP request (transaction data)
      ▼
Azure Function (Python)
      │
      ├── Compute Z-score anomaly
      ├── Store transaction in Azure SQL
      └── If anomaly:
              │
              ▼
        Azure Storage Queue
              │
              ▼
        Azure Logic App
              │
              ▼
        Outlook Email Alert
```

---

## 3. Azure Services Used

| Service                          | Purpose                                          | Tier Used            |
| -------------------------------- | ------------------------------------------------ | -------------------- |
| **Azure Function**               | Serverless anomaly scoring                       | Free (Consumption)   |
| **Azure SQL Database**           | Cloud storage for stats and anomaly transactions | Serverless free tier |
| **Azure Storage Account**        | Queue for anomaly events                         | Free tier            |
| **Azure Queue Storage**          | Message queue for anomalies                      | Free tier            |
| **Azure Logic App**              | Email notification workflow                      | Consumption plan     |
| **Office 365 Outlook Connector** | Email delivery                                   | Free usage           |

---

## 4. Core Design Principles

### 4.1 Event-Driven Architecture

The system reacts to anomalies instead of constantly polling.

```
Transaction → Event → Queue → Workflow → Email
```

This provides:

* Loose coupling between components
* Better scalability
* Simpler error handling
* Asynchronous processing

---

### 4.2 Separation of Concerns

| Component      | Responsibility                       |
| -------------- | ------------------------------------ |
| Django         | User interface and transaction entry |
| Azure Function | Anomaly scoring logic                |
| Azure SQL      | Persistent anomaly data              |
| Queue          | Event messaging                      |
| Logic App      | Notification workflow                |

Each service performs a single, well-defined role.

---

### 4.3 Serverless First Approach

The architecture avoids:

* VM management
* Manual scaling
* Long-running servers

Instead, it uses:

* Function-as-a-Service (FaaS)
* Managed database
* Event-triggered workflows

---

## 5. Anomaly Detection Logic

The system uses a **Z-score statistical model**.

### Concept

For each:

```
(user_id, category_id)
```

We compute:

* Mean transaction amount
* Standard deviation
* Sample count

These statistics form a **baseline**.

---

### Z-Score Formula

```
z = (amount − mean) / standard_deviation
```

---

### Anomaly Rule

A transaction is considered anomalous if:

```
|z_score| > 3
```

This is a standard statistical threshold.

---

### Example

| Mean | Std Dev | New Amount | Z-score | Result  |
| ---- | ------- | ---------- | ------- | ------- |
| 2000 | 500     | 2500       | 1.0     | Normal  |
| 2000 | 500     | 6000       | 8.0     | Anomaly |

---

## 6. Data Flow Summary

### Normal transaction

```
Function receives request
→ Z-score computed
→ Stored in SQL
→ No queue message
→ No email
```

### Anomalous transaction

```
Function receives request
→ Z-score computed
→ Stored in SQL
→ Message pushed to queue
→ Logic App triggered
→ Email sent
```

---

## 7. Key Tables in Azure SQL

### 7.1 anomaly_stats

Stores baseline statistics.

| Column       | Description                |
| ------------ | -------------------------- |
| id           | Primary key                |
| user_id      | User identifier            |
| category_id  | Category identifier        |
| mean         | Average transaction amount |
| std_dev      | Standard deviation         |
| sample_count | Number of samples          |
| created_at   | Timestamp                  |

---

### 7.2 anomaly_transactions

Stores scored transactions.

| Column      | Description            |
| ----------- | ---------------------- |
| id          | Primary key            |
| user_id     | User identifier        |
| category_id | Category identifier    |
| amount      | Transaction amount     |
| z_score     | Computed anomaly score |
| is_anomaly  | Boolean flag           |
| created_at  | Timestamp              |

---
Here is **Part 2** of the documentation.

---

# Finance Tracker – Azure Anomaly Detection Integration

## Project Documentation (Part 2: Azure Setup & Implementation)

---

## 8. Azure Resource Setup

All resources were deployed in the **Central India** region using **free-tier or consumption-based plans**.

### 8.1 Resource Group

A dedicated resource group was created to isolate project resources.

```
Resource Group: finance-track-rg
Region: Central India
```

---

### 8.2 Storage Account

Used for:

* Azure Queue
* Function runtime storage

```
Storage Account Name: financetrackstorage
Type: Standard
Performance: Standard
Redundancy: LRS
```

---

### 8.3 Queue Creation

Inside the storage account, a queue was created:

```
Queue Name: anomaly_alerts
```

Purpose:

* Holds anomaly messages from the Azure Function
* Triggers the Logic App workflow

---

### 8.4 Azure SQL Server & Database

A serverless Azure SQL database was created.

```
SQL Server: financetrack-sql-server
Database: finance-anomaly-db
Compute Tier: Serverless
Region: Central India
```

Authentication:

* SQL admin username
* SQL admin password

Firewall configuration:

* Allowed Azure services
* Allowed local IP for development access

---

## 9. Database Schema Creation

Two tables were created using Azure SQL Query Editor.

---

### 9.1 anomaly_stats Table

Stores precomputed statistics.

```sql
CREATE TABLE anomaly_stats (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    mean FLOAT NOT NULL,
    std_dev FLOAT NOT NULL,
    sample_count INT NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);
```

---

### 9.2 anomaly_transactions Table

Stores scored transactions.

```sql
CREATE TABLE anomaly_transactions (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    amount FLOAT NOT NULL,
    z_score FLOAT,
    is_anomaly BIT,
    created_at DATETIME DEFAULT GETDATE()
);
```

---

## 10. Migrating Anomaly Stats to Azure SQL

Originally, anomaly statistics were stored in:

```
finance/ml/models/anomaly_stats.pkl
```

Structure:

```
{
  user_id: {
    category_id: {
      "mean": float,
      "std": float,
      "count": int
    }
  }
}
```

A custom Django management command was created to:

1. Load the pickle file.
2. Iterate through user/category stats.
3. Insert rows into the `anomaly_stats` table.

Example output:

```
Inserted 350 anomaly stat rows.
```

---

## 11. Azure Function Setup

### 11.1 Function App

```
Function App Name: finance-score-func
Runtime: Python
Plan: Consumption (Serverless)
Region: Central India
```

Deployment method:

```
VS Code → Azure Functions extension
```

---

### 11.2 Function Trigger

HTTP-triggered function:

```
Route: /api/score-transaction
Auth level: function
```

Expected request:

```json
{
  "user_id": 399,
  "category_id": 2310,
  "amount": 25000
}
```

---

## 12. Environment Configuration

Local configuration (`local.settings.json`):

```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",

    "SQL_CONNECTION_STRING": "Driver={ODBC Driver 18 for SQL Server};Server=tcp:financetrack-sql-server.database.windows.net,1433;Database=finance-anomaly-db;Uid=sqladmin;Pwd=YOUR_PASSWORD;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;",

    "AZURE_STORAGE_CONNECTION_STRING": "DefaultEndpointsProtocol=https;AccountName=financetrackstorage;AccountKey=YOUR_KEY;EndpointSuffix=core.windows.net"
  }
}
```

---

## 13. Function Logic

### 13.1 Core Responsibilities

The function performs:

1. Receive transaction data via HTTP.
2. Fetch anomaly statistics from Azure SQL.
3. Compute Z-score.
4. Insert transaction into SQL.
5. Push queue message if anomaly detected.
6. Return JSON response.

---

### 13.2 Z-Score Query

```sql
SELECT mean, std_dev, sample_count
FROM anomaly_stats
WHERE user_id = ? AND category_id = ?
```

---

### 13.3 Transaction Insert

```sql
INSERT INTO anomaly_transactions
(user_id, category_id, amount, z_score, is_anomaly)
VALUES (?, ?, ?, ?, ?)
```

---

### 13.4 Queue Message (if anomaly)

Queue:

```
anomaly_alerts
```

Message example:

```json
{
  "user_id": 399,
  "category_id": 2310,
  "amount": 25000,
  "z_score": 16.9
}
```

---

## 14. Local Testing

Function started locally:

```
func start
```

Test request:

```
POST http://localhost:7071/api/score-transaction
```

Response example:

```json
{
  "user_id": 399,
  "category_id": 2310,
  "amount": 25000.0,
  "z_score": 16.905581089737105,
  "is_anomaly": true
}
```

Verification steps:

1. Confirm row inserted in `anomaly_transactions`.
2. Confirm message appears in `anomaly_alerts` queue.

---

## 15. Function Deployment

The function was deployed to Azure using VS Code.

After deployment:

* Function available at:

```
https://finance-score-func.azurewebsites.net/api/score-transaction
```

* Secured using function key.

---
Here is **Part 3** of the documentation.

---

# Finance Tracker – Azure Anomaly Detection Integration

## Project Documentation (Part 3: Logic App, End-to-End Flow, Testing & Future Improvements)

---

## 16. Logic App Setup

The Logic App is responsible for:

* Listening to the Azure Queue
* Triggering when an anomaly message appears
* Sending an alert notification

---

### 16.1 Logic App Resource

```
Logic App Name: finance-anomaly-alert
Plan: Consumption
Region: Central India
```

---

### 16.2 Trigger Configuration

Trigger type:

```
When a message is received in a queue (Azure Storage)
```

Configuration:

```
Storage account: financetrackstorage
Queue name: anomaly_alerts
Polling interval: 1 minute
```

This means:

* The Logic App checks the queue every minute.
* If a message exists, the workflow starts.

---

### 16.3 Message Parsing

Queue message structure:

```json
{
  "user_id": 399,
  "category_id": 2310,
  "amount": 25000,
  "z_score": 16.9
}
```

A **Parse JSON** action was added with this schema:

```json
{
  "type": "object",
  "properties": {
    "user_id": { "type": "integer" },
    "category_id": { "type": "integer" },
    "amount": { "type": "number" },
    "z_score": { "type": "number" }
  }
}
```

---

### 16.4 Notification Action

An email action was added:

```
Action: Send an email (Office 365 / Outlook / Gmail)
```

Example email content:

```
Subject: Anomaly Detected in Finance Tracker

Body:

An unusual transaction was detected.

User ID: 399
Category ID: 2310
Amount: ₹25,000
Z-score: 16.9

Please review this transaction.
```

---

## 17. End-to-End System Flow

### 17.1 Complete Workflow

1. User records a transaction in Django.
2. Django sends transaction to Azure Function.
3. Azure Function:

   * Fetches stats from SQL
   * Calculates Z-score
   * Stores transaction
   * Pushes queue message if anomaly
4. Logic App detects queue message.
5. Logic App sends email alert.

---

### 17.2 Architecture Summary

```
Django App
   ↓
Azure Function (HTTP trigger)
   ↓
Azure SQL Database (stats + transactions)
   ↓
Azure Queue (if anomaly)
   ↓
Logic App
   ↓
Email Alert
```

---

## 18. Integration with Django

### 18.1 API Call from Django

When a transaction is created:

```python
import requests

url = "https://finance-score-func.azurewebsites.net/api/score-transaction?code=FUNCTION_KEY"

payload = {
    "user_id": user.id,
    "category_id": category.id,
    "amount": float(amount)
}

response = requests.post(url, json=payload)
data = response.json()
```

---

### 18.2 Storing Anomaly Result

Example:

```python
if data.get("is_anomaly"):
    transaction.is_anomaly = True
    transaction.z_score = data.get("z_score")
    transaction.save()
```

---

## 19. Testing the Complete System

### 19.1 Test Case

Input transaction:

```
User ID: 399
Category: Groceries
Normal range: ₹2,000 – ₹5,000
Test amount: ₹25,000
```

---

### 19.2 Expected Behavior

1. Django sends transaction to Function.
2. Function calculates high Z-score.
3. Transaction marked as anomaly.
4. Queue message created.
5. Logic App sends email.

---

### 19.3 Observed Result

Function response:

```json
{
  "user_id": 399,
  "category_id": 2310,
  "amount": 25000.0,
  "z_score": 16.905581089737105,
  "is_anomaly": true
}
```

Outcome:

* Transaction stored in Azure SQL.
* Message added to queue.
* Email alert triggered successfully.

---

## 20. Error Handling Strategy

### 20.1 Missing Statistics

If no stats exist for a category:

```
sample_count < threshold
```

Then:

* Z-score = null
* is_anomaly = false
* Transaction stored normally

---

### 20.2 SQL Connection Failure

Function behavior:

* Log error
* Return HTTP 500
* Django can retry or log failure

---

### 20.3 Queue Failure

If queue message fails:

* Transaction still stored
* Anomaly alert skipped
* Error logged

---

## 21. Cost Optimization Strategy

All services were chosen to minimize cost.

| Service         | Plan         | Cost Model           |
| --------------- | ------------ | -------------------- |
| Azure Function  | Consumption  | Pay per execution    |
| Azure SQL       | Serverless   | Auto-pause when idle |
| Logic App       | Consumption  | Pay per action       |
| Storage Account | Standard LRS | Low fixed cost       |

Estimated monthly cost under light usage:

```
$0 – $5/month
```

---

## 22. Security Considerations

### 22.1 Function Authentication

* Function key required for API calls
* Prevents public abuse

---

### 22.2 SQL Security

* Firewall restricted
* Credentials stored in environment variables

---

### 22.3 Future Security Improvements

* Use Azure Key Vault
* Switch to Managed Identity
* Add API authentication (JWT)

---

## 23. Performance Characteristics

| Component          | Latency        |
| ------------------ | -------------- |
| Django → Function  | ~100–300 ms    |
| SQL query          | ~20–50 ms      |
| Total scoring time | ~150–          |
| –400 ms            |                |
| Logic App trigger  | Up to 1 minute |

---

## 24. Future Improvements

### 24.1 Real-Time Notifications

Replace email with:

* Push notifications
* SMS alerts
* In-app warnings

---

### 24.2 Smarter Anomaly Models

Replace Z-score with:

* Isolation Forest
* Autoencoders
* Time-series models

---

### 24.3 Adaptive Thresholds

* User-specific anomaly sensitivity
* Seasonal adjustments

---

### 24.4 Dashboard Integration

Add:

* Anomaly history
* Category risk indicators
* Spending behavior insights

---

## 25. Key Learnings

1. Serverless architecture reduces infrastructure overhead.
2. Azure Functions are ideal for event-driven ML scoring.
3. Queues decouple detection from notification.
4. Logic Apps provide low-code automation.

---

## 26. Final Outcome

The system successfully:

* Detects abnormal transactions in real time
* Stores anomaly records in the cloud
* Sends automated alerts
* Operates on a serverless, low-cost architecture

---

