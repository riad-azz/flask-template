# Flask modules
from flask_caching import Cache

# Other modules
import os
from dotenv import load_dotenv

load_dotenv()

CACHE_TYPE = os.environ.get("CACHE_TYPE", "SimpleCache")
CACHE_ENABLED = os.environ.get("CACHE_ENABLED", "False") == "True"
CACHE_STORAGE_URL = os.environ.get("CACHE_STORAGE_URL", None)

DEFAULT_CONFIG = {
    "CACHE_TYPE": CACHE_TYPE,
    "CACHE_KEY_PREFIX": "flask_api_cache_",
    "CACHE_DEFAULT_TIMEOUT": 60,
}

cache_config = DEFAULT_CONFIG.copy()

if CACHE_TYPE != "SimpleCache" and CACHE_STORAGE_URL:
    cache_config['CACHE_REDIS_URL'] = CACHE_STORAGE_URL
    cache_config['CACHE_DEFAULT_TIMEOUT'] = 180

cache = Cache(config=cache_config)
