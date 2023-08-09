# Flask modules
from flask import Response

# Local modules
from app.utils.models import SuccessResponse, ErrorResponse


def success_response(data=None, status: int = 200, message: str = None, headers: dict = None, cookies: dict = None,
                     cache_response: bool = False):
    response_data = SuccessResponse(data=data, message=message)
    serialized_data = response_data.to_json()
    response = Response(serialized_data, mimetype="application/json")

    if headers:
        response.headers.update(headers)

    if cache_response:
        cache_header = {"Is-Cached-Response": "1"}
        response.headers.update(cache_header)

    if cookies:
        for key, value in cookies.items():
            response.set_cookie(key, value)

    return response, status


def error_response(message: str = None, status: int = 500, headers: dict = None, cookies: dict = None):
    response_data = ErrorResponse(message=message)
    serialized_data = response_data.to_json()
    response = Response(serialized_data, mimetype="application/json")
    if headers:
        response.headers.update(headers)

    if cookies:
        for key, value in cookies.items():
            response.set_cookie(key, value)

    return response, status
