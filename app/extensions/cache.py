# Flask modules
from flask_caching import Cache

# Other modules
import os
from dotenv import load_dotenv

load_dotenv()

CACHE_REDIS_ENABLED = os.environ.get("CACHE_REDIS_ENABLED", "False") == "True"
CACHE_REDIS_URL = os.environ.get("CACHE_REDIS_URL", None)

DEFAULT_CONFIG = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_KEY_PREFIX": "flask_api_cache_",
    "CACHE_DEFAULT_TIMEOUT": 60,
}

cache_config = DEFAULT_CONFIG.copy()

if CACHE_REDIS_ENABLED and CACHE_REDIS_URL:
    cache_config['CACHE_TYPE'] = 'RedisCache'
    cache_config['CACHE_REDIS_URL'] = CACHE_REDIS_URL
    cache_config['CACHE_DEFAULT_TIMEOUT'] = 180

cache = Cache(config=cache_config)
