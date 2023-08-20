from flask_cors import CORS

CORS_ORIGINS = "*"

cors = CORS(resources={r"/api/*": {"origins": CORS_ORIGINS}})
