import pytest
import requests
import re

BASE_URL = "http://127.0.0.1:5000"


@pytest.fixture(scope="module")
def session():
    return requests.Session()


def test_register_user(session):
    payload = {
        "username": "pytest_user",
        "email": "pytest@example.com",
        "password": "test1234",
        "confirm": "test1234"
    }
    res = session.post(f"{BASE_URL}/register", data=payload, allow_redirects=False)
    assert res.status_code in [200, 201, 302], f"Registration failed: {res.status_code}, {res.text}"


def test_login_user(session):
    payload = {
        "email": "pytest@example.com",
        "password": "test1234"
    }
    res = session.post(f"{BASE_URL}/login", data=payload, allow_redirects=False)
    assert res.status_code in [200, 302], f"Login failed: {res.status_code}, {res.text}"


def test_get_challenges(session):
    res = session.get(f"{BASE_URL}/challenges/")
    assert res.status_code == 200
    assert "Recon 101" in res.text or "Challenge" in res.text


def test_create_review(session):
    # Cette route nécessite que l'utilisateur soit connecté via session cookies
    challenge_id = "63fb443d-0631-4f20-98fb-79ca385b2d8a"  # Doit exister via seed
    payload = {
        "text": "Review test",
        "rating": 4
    }
    res = session.post(f"{BASE_URL}/reviews/challenge/{challenge_id}", data=payload, allow_redirects=False)
    assert res.status_code in [200, 201, 302], f"Review creation failed: {res.status_code}, {res.text}"


def test_get_reviews(session):
    challenge_id = "63fb443d-0631-4f20-98fb-79ca385b2d8a"
    res = session.get(f"{BASE_URL}/reviews/challenge/{challenge_id}", allow_redirects=False)
    assert res.status_code in [200, 302], f"Fetching reviews failed: {res.status_code}, {res.text}"


def test_admin_update_user():
    # Login de l'admin créé dans seed.py
    payload = {
        "email": "admin@att.com",
        "password": "admin1234"
    }
    res = requests.post(f"{BASE_URL}/login", data=payload)
    assert res.status_code == 200

    # Récupération du token depuis la page HTML
    match = re.search(r'"access_token"\s*:\s*"([^"]+)"', res.text)
    if match:
        token = match.group(1)
    else:
        raise Exception("JWT token non trouvé dans la réponse")

    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "username": "updated_admin"
    }
    user_id = "23e6b15d-6f33-4b2d-a29a-556991cb9b59"  # ID de seed.py
    res = requests.put(f"{BASE_URL}/users/{user_id}", json=payload, headers=headers)
    assert res.status_code in [200, 204], f"Admin update failed: {res.status_code}, {res.text}"
