# Other modules
import pytest

# Local modules
from app import create_app
from app.extensions import limiter
from flask_limiter.util import get_remote_address


@pytest.fixture
def app():
    app = create_app()

    limiter.enabled = True
    limiter.reset()

    @app.route("/tests/ratelimit")
    @limiter.limit(key_func=get_remote_address, limit_value="5/minute")
    def index():
        return "Test route"

    return app


def test_rate_limiter(app):
    with app.test_client() as client:
        # Send 5 requests within the rate limit
        for _ in range(5):
            response = client.get("/tests/ratelimit")
            assert response.status_code == 200
            assert response.data.decode("utf-8") == "Test route"

        # Send another request, which should exceed the rate limit
        response = client.get("/tests/ratelimit")
        assert response.status_code == 429
        assert response.headers["Retry-After"] is not None
