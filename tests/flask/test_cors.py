import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app()

    @app.route("/api/test")
    def index():
        return "Test route"

    return app


def test_cors_enabled(app):
    with app.test_client() as client:
        response = client.get("/api/test")
        assert response.status_code == 200
        assert response.headers["Access-Control-Allow-Origin"] is not None
