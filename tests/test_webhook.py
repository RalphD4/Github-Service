# Webhook unit tests written by Pradeep Vuyyuru

import hashlib
import hmac
import json
import os

from backend.app import app


def make_signature(body):
    secret = os.getenv("WEBHOOK_SECRET", "shared_webhook_secret")

    return "sha256=" + hmac.new(
        secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()


def test_valid_signature():
    client = app.test_client()

    body = json.dumps({
        "action": "opened",
        "issue": {"number": 10}
    }).encode()

    response = client.post(
        "/webhook",
        data=body,
        content_type="application/json",
        headers={
            "X-GitHub-Event": "issues",
            "X-GitHub-Delivery": "unit-test-1",
            "X-Hub-Signature-256": make_signature(body)
        }
    )

    assert response.status_code == 204


def test_invalid_signature():
    client = app.test_client()

    body = json.dumps({
        "action": "opened",
        "issue": {"number": 11}
    }).encode()

    response = client.post(
        "/webhook",
        data=body,
        content_type="application/json",
        headers={
            "X-GitHub-Event": "issues",
            "X-GitHub-Delivery": "unit-test-2",
            "X-Hub-Signature-256": "sha256=wrong"
        }
    )

    assert response.status_code == 401


def test_tampered_body():
    client = app.test_client()

    original_body = json.dumps({
        "action": "opened",
        "issue": {"number": 12}
    }).encode()

    tampered_body = json.dumps({
        "action": "closed",
        "issue": {"number": 12}
    }).encode()

    response = client.post(
        "/webhook",
        data=tampered_body,
        content_type="application/json",
        headers={
            "X-GitHub-Event": "issues",
            "X-GitHub-Delivery": "unit-test-3",
            "X-Hub-Signature-256": make_signature(original_body)
        }
    )

    assert response.status_code == 401


def test_duplicate_delivery():
    client = app.test_client()

    body = json.dumps({
        "action": "opened",
        "issue": {"number": 13}
    }).encode()

    headers = {
        "X-GitHub-Event": "issues",
        "X-GitHub-Delivery": "unit-test-duplicate",
        "X-Hub-Signature-256": make_signature(body)
    }

    first = client.post(
        "/webhook",
        data=body,
        content_type="application/json",
        headers=headers
    )

    second = client.post(
        "/webhook",
        data=body,
        content_type="application/json",
        headers=headers
    )

    assert first.status_code == 204
    assert second.status_code == 204

    events = client.get("/events").get_json()

    matches = [
        event for event in events
        if event["delivery_id"] == "unit-test-duplicate"
    ]

    assert len(matches) == 1