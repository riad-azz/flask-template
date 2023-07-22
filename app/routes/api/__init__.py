# Flask modules
from flask import Blueprint, request
from werkzeug.exceptions import HTTPException
from flask_limiter.errors import RateLimitExceeded

# Local modules
from app.extensions import cache, limiter
from app.utils.api import error_response, get_cached_response, make_cache_key

# Blueprint modules
from .tests import tests_bp

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.errorhandler(Exception)
def handle_error(error):
    if isinstance(error, RateLimitExceeded):
        current_limit = error.limit.limit
        return error_response(f"Too many requests: {current_limit}", 429)
    elif isinstance(error, HTTPException):
        return error_response(error.description, error.code)
    else:
        print(error)
        return error_response()


@api_bp.before_request
def before_request():
    # Check if user is rate limited
    limiter.check()

    # Attempt to fetch cached response
    cache_key = make_cache_key(request)
    try:
        cached_response = get_cached_response(cache_key)
        if cached_response is not None:
            return cached_response
    except Exception as e:
        print(f"Error when fetching cached response:", e)


@api_bp.after_request
def after_request(response):
    if response.status_code == 200:
        # Cache the response if it is successful (status code 200)
        try:
            cache_key = make_cache_key(request)
            cache.set(cache_key, response, timeout=300)
        except Exception as e:
            print(f"Error when caching response:", e)
    return response


api_bp.register_blueprint(tests_bp)
