# Other modules
import pytest

# Local modules
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


def test_api_hello(app):
    with app.test_client() as client:
        response = client.get("/api/tests/hello")
        assert response.status_code == 200
        assert response.json["status"] == "success"
        assert response.json["message"] == "Hello World!!"


def test_api_success(app):
    with app.test_client() as client:
        response = client.get("/api/tests/success")
        assert response.status_code == 200
        assert response.json["status"] == "success"
        assert response.json["data"]["title"] == "riad-azz"
        assert response.json["data"]["content"] == "Successful API response"


def test_api_ratelimit(app):
    with app.test_client() as client:
        success_response = client.get("/api/tests/ratelimit")
        limited_response = client.get("/api/tests/ratelimit")

    assert success_response.status_code == 200
    assert success_response.json["status"] == "success"
    assert success_response.json["data"]["title"] == "riad-azz"
    assert success_response.json["data"]["content"] == "Rate limit API response"

    assert limited_response.status_code == 429
    assert limited_response.json["status"] == "error"
    assert limited_response.json["message"] == "Too many requests: 1 per 1 minute"
    assert limited_response.headers["Retry-After"] is not None


def test_api_bad_request(app):
    with app.test_client() as client:
        response = client.get("/api/tests/bad-request")
        assert response.status_code == 400
        assert response.json["status"] == "error"
        assert response.json["message"] == "Bad Request"


def test_api_forbidden(app):
    with app.test_client() as client:
        response = client.get("/api/tests/forbidden")
        assert response.status_code == 403
        assert response.json["status"] == "error"
        assert (
            response.json["message"]
            == "You don't have the permission to access the requested resource"
        )


def test_api_internal_server_error(app):
    with app.test_client() as client:
        response = client.get("/api/tests/internal-server-error")
        assert response.status_code == 500
        assert response.json["status"] == "error"
        assert response.json["message"] == "Internal Server Error"


def test_api_unknown_exception(app):
    with app.test_client() as client:
        response = client.get("/api/tests/unknown-exception")
        assert response.status_code == 500
        assert response.json["status"] == "error"
        assert response.json["message"] == "Internal Server Error"
