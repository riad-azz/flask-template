# Flask modules
import jwt
from flask import current_app

# Other modules
from datetime import datetime, timedelta


def encode_token(user_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=0, seconds=5),
        'iat': datetime.utcnow(),
        'sub': user_id

    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token
