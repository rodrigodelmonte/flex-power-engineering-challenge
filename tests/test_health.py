def test_health(test_app):
    # Given

    # When
    response = test_app.get("/health")

    # Then
    assert response.status_code == 200
    assert response.json() == {"environment": "dev", "health": True, "testing": True}
