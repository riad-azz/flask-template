# Other modules
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / '.env'

load_dotenv(ENV_FILE_PATH)

# Flask
SECRET_KEY = os.environ.get("SECRET_KEY", "YOUR-FALLBACK-SECRET-KEY")
DATABASE_URI = "sqlite:///database.db"
# Ratelimit
RATELIMIT_ENABLED = os.environ.get("RATELIMIT_ENABLED", "False") == "True"
RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI", "memory://")


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
