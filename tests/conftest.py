import pytest
from fastapi.testclient import TestClient

from flexpower.config import Settings, get_settings
from flexpower.main import create_application

override_settings = Settings(testing=True)


@pytest.fixture(scope="session")
def test_app():
    app = create_application()
    client = TestClient(app)
    app.dependency_overrides[get_settings] = lambda: override_settings
    with client as _test_app:
        yield _test_app
