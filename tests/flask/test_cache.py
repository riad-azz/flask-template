# Other modules
import os
import pytest

# Local modules
from app import create_app
from app.utils.cache import get_cached_response


@pytest.fixture
def app():
    DEBUG = os.environ.get("DEBUG", "False") == "True"
    app = create_app(debug=DEBUG)

    return app


def test_api_cache(app):
    request_url = "/api/tests/cached"
    with app.test_client() as client:
        response = client.get(request_url)
        assert response.status_code == 200
        assert response.json["status"] == "success"
        assert response.json["data"]["title"] == "riad-azz"
        assert response.json["data"]["content"] == "Cached API response"

    request = response.request
    is_cached = get_cached_response(request)

    assert bool(is_cached) is True
