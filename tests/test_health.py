from fastapi.testclient import TestClient


def test_health(client: TestClient):
    # Given

    # When
    response = client.get("/health")

    # Then
    assert response.status_code == 200
    assert response.json() == {"environment": "dev", "health": True, "testing": True}
