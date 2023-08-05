# Flask modules
from flask import Blueprint

# Local modules
from app.extensions import db
from app.models.user import User
from app.utils.api import success_response, error_response

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=['POST'])
def login():
    pass


@auth_bp.route("/register", methods=['POST'])
def register():
    pass


@auth_bp.route("/logout")
def logout():
    pass
