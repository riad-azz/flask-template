# Other modules
import uuid
from datetime import datetime

# Local modules
from app.extensions import db


def generate_uuid():
    return str(uuid.uuid4())


class User(db.Model):
    __table_name = 'users'

    id = db.Column(db.String, primary_key=True, default=generate_uuid, unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.name}>'
