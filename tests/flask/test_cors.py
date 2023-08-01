# Other modules
import os
import pytest

# Local modules
from app import create_app


@pytest.fixture
def app():
    DEBUG = os.environ.get("DEBUG", "False") == "True"
    app = create_app(debug=DEBUG)

    return app


def test_cors_enabled(app):
    with app.test_client() as client:
        response = client.get("/api/tests/success")
        assert response.status_code == 200
        assert response.headers["Access-Control-Allow-Origin"] is not None
