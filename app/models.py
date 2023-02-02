# Flask modules
from flask_login import UserMixin

# App modules
from app import db, bcrypt


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email = db.Column(db.String(length=255), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, plain_password: str):
        self.password_hash = bcrypt.generate_password_hash(plain_password).decode('utf-8')

    def __repr__(self):
        return f'<User {self.id}>'
