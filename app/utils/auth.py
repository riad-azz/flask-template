# Flask modules
import jwt
from flask import current_app

# Other modules
from datetime import datetime, timedelta


def encode_token(user_id: str):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=30),
        'iat': datetime.utcnow(),
        'user_id': user_id,
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token


def decode_token(token: str):
    data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    return data
