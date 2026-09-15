## Validation testing written by Vishnu Vennelakanti

import json

from backend.app import app


def test_missing_title():
    client = app.test_client()

    response = client.post(
        "/issues",
        data=json.dumps({"body": "no title"}),
        content_type="application/json",
    )

    assert response.status_code == 400


def test_invalid_issue():
    client = app.test_client()

    response = client.post(
        "/issues",
        data=json.dumps({"title": "example title", "labels": "[wrong type]"}),
        content_type="application/json",
    )

    assert response.status_code == 400


def test_invalid_state():
    client = app.test_client()

    response = client.patch(
        "/issues/1",
        data=json.dumps({"state": "archived"}),
        content_type="application/json",
    )

    assert response.status_code == 400


def test_empty_payload():
    client = app.test_client()

    response = client.patch(
        "/issues/1",
        data=json.dumps({}),
        content_type="application/json",
    )

    assert response.status_code == 400


def test_invalid_title_type():
    client = app.test_client()

    response = client.patch(
        "/issues/1",
        data=json.dumps({"title": 12345}),
        content_type="application/json",
    )

    assert response.status_code == 400


def test_comment_nobody():
    client = app.test_client()

    response = client.post(
        "/issues/1/comments",
        data=json.dumps({"nobody": ""}),
        content_type="application/json",
    )

    assert response.status_code == 400