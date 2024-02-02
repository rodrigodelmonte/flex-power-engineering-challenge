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


def test_get_trades_by_delivery_day(client: TestClient):
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
    client.post("/v1/trades", json=data)

    response = client.get("/v1/trades?delivery_day=2024-02-01")

    assert response.status_code == 200
    assert response.json()[0]["id"] == "trade_123"


def test_get_trades_by_trade_id(client: TestClient):
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
    client.post("/v1/trades", json=data)

    response = client.get("/v1/trades?trade_id=MirkoT")

    assert response.status_code == 200
    assert response.json()[0]["id"] == "trade_123"


def test_get_trades_missing_query_parameters(client: TestClient):
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
    client.post("/v1/trades", json=data)

    response = client.get("/v1/trades")

    assert response.status_code == 404
    assert response.json()["detail"] == "provide trade_id or delivery_day as query parameter"


def test_get_trades_by_trade_id_not_found(client: TestClient):
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
    client.post("/v1/trades", json=data)

    response = client.get("/v1/trades?trade_id=not_exists")

    assert response.status_code == 404
    assert response.json()["detail"] == "not found"


def test_get_trades_by_delivery_day_not_found(client: TestClient):
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
    client.post("/v1/trades", json=data)

    response = client.get("/v1/trades?delivery_day=0000-00-00")

    assert response.status_code == 404
    assert response.json()["detail"] == "not found"
