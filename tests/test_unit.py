import json
import requests

from backend.app import app
from backend.services.github_service import OWNER, REPO

test_url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"

client_conn = app.test_client()

def test_404():
    requests.add(requests.GET, 
                 f"{test_url}/10000", 
                 payload={"message": "404 not found"}, 
                 status=404)
    response = client_conn.get("/issues/10000")

    if response.status_code != 404 or response.get_json()["error"] != "issue not found":
        raise AssertionError



def test_401():
    requests.add(requests.POST, 
                 test_url, 
                 payload={"message": "401 invalid credentials"}, 
                 status=401)
    
    response = client_conn.post(
        "/issues",
        data=json.dumps({"title": "test issue"}),
        content_type="application/json",
    )

    if response.status_code != 401:
        raise AssertionError


def test_403():
    requests.add(
        requests.GET,
        test_url,
        payload={"message": "rate limit exceeded"},
        status=403,
        headers={"X-RateLimit-Remaining": "0", "X-RateLimit-Reset": "10000"},
    )

    response = client_conn.get("/issues")
    if response.status_code != 429 or "Retry-After" not in response.headers:
        raise AssertionError



def test_429():
    requests.add(
        requests.GET,
        test_url,
        payload={"message": "rate limited"},
        status=429,
        headers={"Retry-After": "30"},
    )
    response = client_conn.get("/issues")
    assert response.status_code == 429
    if response.status_code != 429 or response.headers["Retry-After"] != "15" :
        raise AssertionError
    

def test_500():
    requests.add(requests.GET, test_url, 
                 payload={"message": "500 internal error"}, 
                 status=500)
    response = client_conn.get("/issues")
    if response.status_code != 500:
        raise AssertionError