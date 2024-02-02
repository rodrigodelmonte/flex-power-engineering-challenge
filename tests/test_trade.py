from fastapi.testclient import TestClient


def test_create_trade(client: TestClient):
    data = {
        "id": "trade_123",
        "price": 200,
        "quantity": 12,
        "direction": "buy",
        "delivery_day": "2024-02-01",
        "delivery_hour": 14,
        "trader_id": "MirkoT",
        "execution_time": "2024-02-01T10:30:00Z",
    }

    response = client.post("/v1/trades", json=data)

    assert response.status_code == 201


def test_create_trade_invalid_payload(client: TestClient):
    data = {
        "id": "trade_123",
        "price": 200,
        "quantity": 12,
        "direction": "buy",
        "delivery_day": "2024-02-01",
        "delivery_hour": 14,
        "trader_id": "MirkoT",
        "execution_time": True,
    }

    response = client.post("/v1/trades", json=data)

    assert response.status_code == 422
    assert response.json()["status_code"] == 422
    assert response.json()["message"] is not None
    assert response.json()["message"][0]["field"] == "execution_time"
    assert response.json()["message"][0]["field_type"] == "string_type"
    assert response.json()["message"][0]["error_message"] == "Input should be a valid string"
