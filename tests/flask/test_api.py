import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app()

    return app


def test_api_success(app):
    with app.test_client() as client:
        response = client.get("/api/example/success")
        assert response.status_code == 200
        assert response.json["status"] == "success"
        assert response.json["data"]["response"] == "Successful API response"


def test_api_bad_request(app):
    with app.test_client() as client:
        response = client.get("/api/example/bad-request")
        assert response.status_code == 400
        assert response.json["status"] == "error"
        assert response.json["message"] == "Bad Request"


def test_api_internal_sever_error(app):
    with app.test_client() as client:
        response = client.get("/api/example/internal-server-error")
        assert response.status_code == 500
        assert response.json["status"] == "error"
        assert response.json["message"] == "Internal Server Error"
