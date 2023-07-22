# Flask modules
from flask import Blueprint
from werkzeug.exceptions import BadRequest, InternalServerError, Forbidden

# Local modules
from app.extensions import limiter
from app.models.test import TestModel
from app.utils.api import success_response

tests_bp = Blueprint("tests", __name__, url_prefix="/tests")


@tests_bp.route("/success", methods=["GET"])
@limiter.exempt
def test_api_success():
    data = TestModel(title="riad-azz", content="Successful API response")
    return success_response(data, 200)


@tests_bp.route("/cached", methods=["GET"])
@limiter.exempt
def test_api_cached():
    data = TestModel(title="riad-azz", content="Cached API response")
    return success_response(data, 200)


@tests_bp.route("/bad-request", methods=["GET"])
@limiter.exempt
def test_api_bad_request():
    raise BadRequest("Bad Request")


@tests_bp.route("/forbidden", methods=["GET"])
@limiter.exempt
def test_api_forbidden():
    raise Forbidden("You don't have the permission to access the requested resource")


@tests_bp.route("/internal-server-error", methods=["GET"])
@limiter.exempt
def test_api_internal_server_error():
    raise InternalServerError("Internal Server Error")


@tests_bp.route("/unknown-exception", methods=["GET"])
@limiter.exempt
def test_api_unknown_error():
    raise Exception("Unknown Exception")
