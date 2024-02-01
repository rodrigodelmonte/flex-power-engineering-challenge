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
