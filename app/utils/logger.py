# Other modules
import os
from pathlib import Path
from logging.config import dictConfig

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_FILENAME = "app.log"
LOG_FOLDER_DIR = BASE_DIR / "logs"
LOG_FILE_PATH = os.path.join(LOG_FOLDER_DIR, LOG_FILENAME)


def setup_flask_logger():
    if not os.path.isdir(LOG_FOLDER_DIR):
        os.makedirs(LOG_FOLDER_DIR)

    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s : %(message)s",
                }
            },
            "handlers": {
                "file": {
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "formatter": "default",
                    "filename": LOG_FILE_PATH,
                    "backupCount": 2,
                },
                "wsgi": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "default",
                },
            },
            "root": {"level": "DEBUG", "handlers": ["file", "wsgi"]},
        }
    )
