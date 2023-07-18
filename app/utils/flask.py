# Flask modules
from flask import Response

# Local modules
from app.models.api import SuccessResponse, ErrorResponse


def json_response(data, status: int = 200):
    response_data = SuccessResponse(data=data)
    serialized_data = response_data.to_json()
    response = Response(serialized_data, mimetype="application/json")
    return response, status


def error_response(message: str = "Internal Server Error", status: int = 500):
    response_data = ErrorResponse(message=message)
    serialized_data = response_data.to_json()
    response = Response(serialized_data, mimetype="application/json")
    return response, status
