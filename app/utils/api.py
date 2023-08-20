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


def success_response(
    data=None,
    status: int = 200,
    message: str = None,
    headers: dict = None,
    cookies: dict = None,
    cache_response: bool = False,
):
    """
    Generate a success response with the provided data, status code, message, headers, cookies, and cache response flag.

    Parameters:
        data (Any, optional): The data to be included in the response. Defaults to None.
        status (int, optional): The status code of the response. Defaults to 200.
        message (str, optional): The message to be included in the response. Defaults to None.
        headers (dict, optional): The headers to be included in the response. Defaults to None.
        cookies (dict, optional): The cookies to be included in the response. Defaults to None.
        cache_response (bool, optional): Flag to indicate if the response should be cached. Defaults to False.

    Returns:
        tuple: A tuple containing the response object and the status code.
            - response (Response): The success response object.
            - status (int): The status code of the response.
    """
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


def error_response(
    message: str = "Internal Server Error",
    status: int = 500,
    headers: dict = None,
    cookies: dict = None,
):
    """
    Generate an error response with the given message, status code, headers, and cookies.

    Parameters:
        message (str): The error message to be included in the response. Defaults to "Internal Server Error".
        status (int): The status code to be included in the response. Defaults to 500.
        headers (dict): A dictionary of additional headers to be included in the response. Defaults to None.
        cookies (dict): A dictionary of cookies to be included in the response. Defaults to None.

    Returns:
        tuple: A tuple containing the response object and the status code.
            - response (Response): The error response object.
            - status (int): The status code of the response.
    """
    response_data = ErrorResponse(message=message)
    serialized_data = response_data.to_json()
    response = Response(serialized_data, mimetype="application/json")

    if headers:
        response.headers.update(headers)

    if cookies:
        for key, value in cookies.items():
            response.set_cookie(key, value)

    return response, status
