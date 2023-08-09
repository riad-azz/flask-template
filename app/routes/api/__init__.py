# Flask modules
from flask import Blueprint, request
from flask_limiter import ExemptionScope
from werkzeug.exceptions import HTTPException
from flask_limiter.errors import RateLimitExceeded

# Other modules
import logging

# Local modules
from app.extensions import limiter
from app.utils.api import error_response

# Blueprint modules
from .tests import tests_bp

api_bp = Blueprint("api", __name__, url_prefix="/api")
limiter.exempt(api_bp, flags=ExemptionScope.DEFAULT |
                             ExemptionScope.APPLICATION |
                             ExemptionScope.DESCENDENTS)


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


api_bp.register_blueprint(tests_bp)
