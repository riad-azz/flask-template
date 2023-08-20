# Other modules
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"

load_dotenv(ENV_FILE_PATH)

# Flask
SECRET_KEY = os.environ.get("SECRET_KEY", "YOUR-FALLBACK-SECRET-KEY")
DATABASE_URI = "sqlite:///database.db"
# Ratelimit
RATELIMIT_ENABLED = os.environ.get("RATELIMIT_ENABLED", "False") == "True"
RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI", "memory://")
# Caching
CACHE_TYPE = os.environ.get("CACHE_TYPE", "SimpleCache")
CACHE_ENABLED = os.environ.get("CACHE_ENABLED", "False") == "True"
CACHE_STORAGE_URL = os.environ.get("CACHE_STORAGE_URL", None)
CACHE_EXEMPTED_ROUTES = [
    "/api/auth/",
]


class ProdConfig:
    # Flask
    TESTING = False
    DEBUG = False
    TEMPLATES_AUTO_RELOAD = False
    STATIC_AUTO_RELOAD = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "YOUR-FALLBACK-SECRET-KEY")
    # Database
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    # Ratelimit
    RATELIMIT_ENABLED = RATELIMIT_ENABLED
    RATELIMIT_STORAGE_URI = RATELIMIT_STORAGE_URI
    RATELIMIT_STRATEGY = "fixed-window"  # or "moving-window"
    RATELIMIT_IN_MEMORY_FALLBACK_ENABLED = True
    RATELIMIT_HEADERS_ENABLED = True
    # Caching
    CACHE_ENABLED = CACHE_ENABLED
    CACHE_TYPE = CACHE_TYPE
    CACHE_KEY_PREFIX = "flask_cache_"
    CACHE_EXEMPTED_ROUTES = CACHE_EXEMPTED_ROUTES
    if CACHE_TYPE != "SimpleCache" and CACHE_STORAGE_URL:
        CACHE_REDIS_URL = CACHE_STORAGE_URL
        CACHE_DEFAULT_TIMEOUT = 180
    else:
        CACHE_DEFAULT_TIMEOUT = 60
