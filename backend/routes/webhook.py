# Webhook routes and handling written by Pradeep Vuyyuru

import hashlib
import hmac
import os
import sqlite3

from flask import Blueprint, jsonify, request
from datetime import datetime

webhook_api = Blueprint("webhook", __name__)


def check_signature(body, signature):
    secret = os.getenv("WEBHOOK_SECRET")

    if not secret or not signature:
        return False

    expected = "sha256=" + hmac.new(
        secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, signature)


def save_event(delivery_id, event, action, issue_number):
    conn = sqlite3.connect("backend/database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS webhook_events (
            delivery_id TEXT PRIMARY KEY,
            event TEXT,
            action TEXT,
            issue_number INTEGER,
            timestamp TEXT
        )
    """)

    try:
        cursor.execute("""
            INSERT INTO webhook_events
            VALUES (?, ?, ?, ?, ?)
        """, (delivery_id, event, action, issue_number,datetime.now().isoformat()))

        conn.commit()

    except sqlite3.IntegrityError:
        pass

    conn.close()


@webhook_api.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_data()

    signature = request.headers.get("X-Hub-Signature-256")
    event = request.headers.get("X-GitHub-Event")
    delivery_id = request.headers.get("X-GitHub-Delivery")

    if not check_signature(body, signature):
        return jsonify({"error": "Invalid signature"}), 401

    if event not in ["issues", "issue_comment", "ping"]:
        return jsonify({"error": "Unknown event"}), 400

    data = request.get_json()

    if event == "ping":
        action = "ping"
        issue_number = None
    else:
        action = data.get("action")

        if not action:
            return jsonify({"error": "Unknown action"}), 400

        issue_number = data.get("issue", {}).get("number")

    save_event(delivery_id, event, action, issue_number)

    print("Webhook:", delivery_id, event, action, issue_number)

    return "", 204


@webhook_api.route("/events", methods=["GET"])
def get_events():
    conn = sqlite3.connect("backend/database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS webhook_events (
            delivery_id TEXT PRIMARY KEY,
            event TEXT,
            action TEXT,
            issue_number INTEGER,
            timestamp TEXT
        )
    """)

    cursor.execute("""
        SELECT *
        FROM webhook_events
        ORDER BY rowid DESC
        LIMIT 20
    """)

    rows = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows]), 200