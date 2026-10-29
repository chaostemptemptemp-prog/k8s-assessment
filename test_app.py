import pytest
from app import app

@pytest.fixture(autouse=True)
def reset_balance():
    app.balance = 0.0
    yield
    app.balance = 0.0

def test_home_page():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Simple Banking Application"
    assert response.get_json()["balance"] == 0.0

def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"

def test_check_balance():
    app.balance = 250.0
    client = app.test_client()
    response = client.get("/balance")
    assert response.status_code == 200
    assert response.get_json()["balance"] == 0

def test_deposit_success():
    client = app.test_client()
    response = client.post("/deposit", json={"amount": 100})
    assert response.status_code == 200
    assert response.get_json()["balance"] == 100.0

def test_deposit_invalid_amount():
    client = app.test_client()
    response = client.post("/deposit", json={"amount": -10})
    assert response.status_code == 400
    assert "greater than zero" in response.get_json()["error"]