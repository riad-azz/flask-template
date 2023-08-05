# Flask modules
from flask import Response

# Local modules
from app.utils.models import SuccessResponse, ErrorResponse


def success_response(data: str | dict = None, status: int = 200):
    if type(data) == str or data is None:
        message = data or ""
        data = {"message": message}
    else:
        data = {"data": data}
    response_data = SuccessResponse(data=data)
    serialized_data = response_data.to_json()
    response = Response(serialized_data, mimetype="application/json")
    return response, status


def error_response(data: str | dict = None, status: int = 500):
    if data is None or type(data) == str:
        message = data or "Internal Server Error"
        data = {"message": message}
    response_data = ErrorResponse(data=data)
    serialized_data = response_data.to_json()
    response = Response(serialized_data, mimetype="application/json")
    return response, status
