import copy
import importlib
import pytest
from fastapi.testclient import TestClient

# Import the app module dynamically to avoid import issues
app_module = importlib.import_module("src.app")


@pytest.fixture
def app():
    return app_module.app


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Deep-copy and restore the global `activities` dict around each test.

    This fixture runs automatically for every test to ensure isolation.
    """
    original = copy.deepcopy(app_module.activities)
    try:
        yield
    finally:
        app_module.activities.clear()
        app_module.activities.update(original)
