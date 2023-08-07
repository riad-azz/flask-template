# Flask modules
from flask_jwt_extended import get_current_user

# Other modules
from datetime import datetime

# Local modules
from app.extensions import db
from app.utils.auth import generate_uuid


class User(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid, unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    token_version = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    type = db.Column(db.String(16), nullable=False)
    user_id = db.Column(
        db.ForeignKey('user.id'),
        default=lambda: get_current_user().id,
        nullable=False,
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
