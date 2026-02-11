import azure.functions as func
import json
import logging
import os
import pyodbc
from azure.storage.queue import QueueClient

app = func.FunctionApp()

# ---------- Helper: SQL connection ----------
def get_sql_connection():
    conn_str = os.environ["SQL_CONNECTION_STRING"]
    return pyodbc.connect(conn_str)


# ---------- Helper: Load anomaly stats ----------
def get_anomaly_stats(conn, user_id, category_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT mean, std_dev, sample_count
        FROM anomaly_stats
        WHERE user_id = ? AND category_id = ?
    """, (user_id, category_id))

    row = cursor.fetchone()
    return row


# ---------- Helper: Insert transaction ----------
def insert_transaction(conn, user_id, category_id, amount, z_score, is_anomaly):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO anomaly_transactions (user_id, category_id, amount, z_score, is_anomaly)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, category_id, amount, z_score, is_anomaly))
    conn.commit()


# ---------- Helper: Send queue message ----------
def send_queue_message(payload):
    queue_conn = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    queue_name = "anomaly-alerts"

    queue = QueueClient.from_connection_string(queue_conn, queue_name)
    queue.send_message(json.dumps(payload))


# ---------- Main HTTP function ----------
@app.route(route="score-transaction", auth_level=func.AuthLevel.FUNCTION)
def score_transaction(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("score-transaction: Processing finance request")

    try:
        body = req.get_json()
        user_id = int(body["user_id"])
        category_id = int(body["category_id"])
        amount = float(body["amount"])
    except Exception:
        return func.HttpResponse(
            json.dumps({"error": "Invalid request body"}),
            status_code=400,
            mimetype="application/json"
        )

    try:
        conn = get_sql_connection()

        # Get stats
        stats = get_anomaly_stats(conn, user_id, category_id)

        if stats:
            mean, std_dev, sample_count = stats

            if std_dev == 0:
                z_score = 0
            else:
                z_score = (amount - mean) / std_dev

        else:
            z_score = 0

        is_anomaly = abs(z_score) > 3

        # Insert transaction
        insert_transaction(conn, user_id, category_id, amount, z_score, is_anomaly)

        # If anomaly → push to queue
        if is_anomaly:
            queue_payload = {
                "user_id": user_id,
                "category_id": category_id,
                "amount": amount,
                "z_score": z_score
            }
            send_queue_message(queue_payload)

        response = {
            "user_id": user_id,
            "category_id": category_id,
            "amount": amount,
            "z_score": z_score,
            "is_anomaly": is_anomaly
        }

        return func.HttpResponse(
            json.dumps(response),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(
            json.dumps({"error": "Server error", "details": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
