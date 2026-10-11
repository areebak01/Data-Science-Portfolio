
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Make backend modules importable
BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_DIR))


@pytest.fixture
def client():
    from main import app

    return TestClient(app)
