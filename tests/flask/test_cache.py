# Other modules
import pytest

# Local modules
from app import create_app
from app.utils.api import get_cached_response


@pytest.fixture
def app():
    app = create_app()

    return app


def test_api_cache(app):
    request_url = "/api/tests/cached"
    with app.test_client() as client:
        response = client.get(request_url)
        assert response.status_code == 200
        assert response.json["status"] == "success"
        assert response.json["data"]["title"] == "riad-azz"
        assert response.json["data"]["content"] == "Cached API response"

    is_cached = get_cached_response(response.request.url)
    assert bool(is_cached) is True
