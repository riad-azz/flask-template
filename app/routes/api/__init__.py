# Flask modules
from flask import Blueprint, request
from flask.wrappers import Response
from flask_limiter import ExemptionScope
from werkzeug.exceptions import HTTPException
from flask_limiter.errors import RateLimitExceeded

# Other modules
import logging

# Local modules
from app.extensions import limiter
from app.utils.api import error_response
from app.utils.cache import get_cached_response, set_cached_response

# Blueprint modules
from .tests import tests_bp

api_bp = Blueprint("api", __name__, url_prefix="/api")
limiter.exempt(
    api_bp,
    flags=ExemptionScope.DEFAULT
    | ExemptionScope.APPLICATION
    | ExemptionScope.DESCENDENTS,
)


@api_bp.errorhandler(Exception)
def handle_error(error):
    if isinstance(error, RateLimitExceeded):
        current_limit = error.limit.limit
        return error_response(f"Too many requests: {current_limit}", 429)
    elif isinstance(error, HTTPException):
        return error_response(error.description, error.code)
    else:
        logging.error(error)
        return error_response()


@api_bp.before_request
def before_request():
    # Attempt to fetch cached response
    cached_response = get_cached_response(request)
    if cached_response is not None:
        return cached_response


@api_bp.after_request
def after_request(response: Response):
    if response.headers.get("Is-Cached-Response") == "1":
        # Remove internal cache header
        response.headers.remove("Is-Cached-Response")
        # Cache the response
        set_cached_response(request, response)
    return response


api_bp.register_blueprint(tests_bp)
