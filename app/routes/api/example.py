# Flask modules
from flask import Blueprint

# Other modules
from werkzeug.exceptions import BadRequest, InternalServerError

# Local modules
from app.utils.flask import json_response

example_bp = Blueprint("example", __name__, url_prefix="/example")


@example_bp.route("/success", methods=["GET"])
def example_api_success():
    data = {"response": "Successful API response"}
    return json_response(data, 200)


@example_bp.route("/bad-request", methods=["GET"])
def example_api_bad_request():
    raise BadRequest("Bad Request")


@example_bp.route("/internal-server-error", methods=["GET"])
def example_api_internal_server_error():
    raise InternalServerError("Internal Server Error")
