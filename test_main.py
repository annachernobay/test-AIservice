from fastapi.testclient import TestClient
from main import app
from pricing import calculate_cost

client = TestClient(app)


def test_calculate_cost():
    # 1,000,000 prompt tokens ($0.15) + 1,000,000 completion tokens ($0.60) = $0.75
    cost = calculate_cost("gpt-4o-mini", 1000000, 1000000)
    assert cost == 0.75


def test_create_session():
    response = client.post("/sessions", json={"model": "gpt-4o-mini"})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["model"] == "gpt-4o-mini"
    assert data["total_cost_usd"] == 0.0


def test_get_nonexistent_session():
    response = client.get("/sessions/invalid-uuid-12345")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"] == "SESSION_NOT_FOUND"