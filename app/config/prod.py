import os
from dotenv import load_dotenv

load_dotenv()


class ProdConfig:
    TESTING = False
    DEBUG = False
    TEMPLATES_AUTO_RELOAD = False
    STATIC_AUTO_RELOAD = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "YOUR-FALLBACK-SECRET-KEY")
