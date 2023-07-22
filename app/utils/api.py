# Flask modules
from flask import Response
from flask.wrappers import Request

# Local modules
from app.extensions import cache
from app.utils.models import SuccessResponse, ErrorResponse


def make_cache_key(request: Request):
    full_url = request.url
    api_cache_url = full_url.split("/api/")[-1]
    return api_cache_url


def get_cached_response(cache_key: str):
    return cache.get(cache_key)


def success_response(data, status: int = 200):
    response_data = SuccessResponse(data=data)
    serialized_data = response_data.to_json()
    response = Response(serialized_data, mimetype="application/json")
    return response, status


def error_response(message: str = "Internal Server Error", status: int = 500):
    response_data = ErrorResponse(message=message)
    serialized_data = response_data.to_json()
    response = Response(serialized_data, mimetype="application/json")
    return response, status
