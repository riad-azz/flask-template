# Flask modules
from flask import Response

# Local modules
from app.utils.models import SerializableClass


class APIResponse(SerializableClass):

    def __init__(self, status: str, message: str, data=None):
        self.status = status
        self.message = message
        self.data = data

    def to_dict(self):
        response_dict = dict()
        response_dict["status"] = self.status

        if self.message:
            response_dict["message"] = self.message

        if self.data:
            if not SerializableClass.is_serializable(self.data):
                raise TypeError(f"{self.data} is not json serializable")
            response_dict["data"] = self.data

        return response_dict


class SuccessResponse(APIResponse):
    def __init__(self, data=None, message: str = None):
        super().__init__(status="success", message=message, data=data)


class ErrorResponse(APIResponse):
    def __init__(self, message: str = None):
        super().__init__(status="error", message=message)


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


def error_response(message: str = "Internal Server Error", status: int = 500, headers: dict = None,
                   cookies: dict = None):
    response_data = ErrorResponse(message=message)
    serialized_data = response_data.to_json()
    response = Response(serialized_data, mimetype="application/json")

    if headers:
        response.headers.update(headers)

    if cookies:
        for key, value in cookies.items():
            response.set_cookie(key, value)

    return response, status
