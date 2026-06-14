import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture()
def client():
    """Provide a TestClient and restore `activities` after each test."""
    original = copy.deepcopy(app_module.activities)
    client = TestClient(app_module.app)
    yield client
    # Restore the in-memory activities to avoid test cross-talk
    app_module.activities.clear()
    app_module.activities.update(original)
