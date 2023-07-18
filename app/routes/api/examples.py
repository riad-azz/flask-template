# Flask modules
from flask import Blueprint
from werkzeug.exceptions import BadRequest, InternalServerError

# Local modules
from app.models.example import ExampleModel
from app.utils.api import success_response

examples_bp = Blueprint("examples", __name__, url_prefix="/examples")


@examples_bp.route("/success", methods=["GET"])
def example_api_success():
    data = ExampleModel(title="riad-azz", content="Successful API response")
    return success_response(data, 200)


@examples_bp.route("/bad-request", methods=["GET"])
def example_api_bad_request():
    raise BadRequest("Bad Request")


@examples_bp.route("/internal-server-error", methods=["GET"])
def example_api_internal_server_error():
    raise InternalServerError("Internal Server Error")


@examples_bp.route("/unknown-exception", methods=["GET"])
def example_api_unknown_error():
    raise Exception("Unknown Exception")
