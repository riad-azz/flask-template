# Flask modules
from flask.wrappers import Request

# Local modules
from app.extensions import cache


def make_cache_key(request: Request):
    full_url = request.url
    api_cache_url = full_url.split("/api/")[-1]
    return api_cache_url


def get_cached_response(cache_key: str):
    return cache.get(cache_key)
