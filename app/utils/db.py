# Local modules
from app.extensions import db

# Models
from app.models.user import User


def create_tables(app):
    with app.app_context():
        db.create_all()
