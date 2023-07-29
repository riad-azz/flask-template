# Flask modules
from flask.wrappers import Request, Response

# Other modules
import os
from dotenv import load_dotenv

# Local modules
from app.extensions import cache

load_dotenv()

CACHE_ENABLED = os.environ.get("CACHE_ENABLED", "False") == "True"


def make_api_cache_key(request: Request):
    full_url = request.url
    api_cache_url = full_url.split("/api/")[-1]
    return api_cache_url


def get_cached_response(request: Request):
    if not CACHE_ENABLED:
        return
    cache_key = make_api_cache_key(request)
    try:
        cached_response = cache.get(cache_key)
        if cached_response is not None:
            return cached_response
    except Exception as e:
        print(f"Error when fetching cached response:", e)

    return None


def set_cached_response(request: Request, response: Response):
    if not CACHE_ENABLED:
        return
    try:
        cache_key = make_api_cache_key(request)
        if not cache.get(cache_key):
            cache.set(cache_key, response)
    except Exception as e:
        print(f"Error when caching response:", e)