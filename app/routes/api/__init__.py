# Flask modules
from werkzeug.exceptions import HTTPException

from flask import Blueprint
from flask_limiter.errors import RateLimitExceeded

# Local modules
from app.utils.flask import error_response

# Blueprint modules
from .example import example_bp

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.errorhandler(Exception)
def handle_error(error):
    if isinstance(error, HTTPException):
        return error_response(error.description, error.code)
    else:
        return error_response()


@api_bp.errorhandler(429)
def handle_rate_limit_exceeded(e):
    if isinstance(e, RateLimitExceeded):
        current_limit = e.limit.limit
        return error_response(f"Too many requests: {current_limit}", 429)
    else:
        return error_response("Too many requests, please try again later", 429)


api_bp.register_blueprint(example_bp)
