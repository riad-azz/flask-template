# Flask modules
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest, Conflict, InternalServerError

# Other modules
import logging
from datetime import datetime
from email_validator import validate_email, EmailNotValidError

# Local modules
from app.extensions import db
from app.utils.api import success_response
from app.utils.auth import generate_jwt_token
from app.models.auth import User, TokenBlocklist

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=['POST'])
def login():
    user_data = request.get_json()
    email = user_data.get("email")
    password = user_data.get("password")

    if not email:
        raise BadRequest("Email address is required")
    elif not password:
        raise BadRequest("Password is required")

    try:
        validated_email = validate_email(email)
    except EmailNotValidError:
        raise BadRequest("Invalid email address")

    clean_email = validated_email.normalized.lower()

    user = User.query.filter_by(email=clean_email).first()
    if not user:
        raise BadRequest("User does not exist")

    if not check_password_hash(user.password, password):
        raise BadRequest("Invalid credentials")

    access_token = generate_jwt_token(user)
    data = {'access_token': access_token}

    return success_response(data=data, message="Successfully logged in", status=201)


@auth_bp.route("/register", methods=['POST'])
def register():
    user_data = request.get_json()
    email = user_data.get("email")
    password = user_data.get("password")

    if not email:
        raise BadRequest("Email address is required")
    elif not password:
        raise BadRequest("Password is required")

    try:
        validated_email = validate_email(email)
    except EmailNotValidError:
        raise BadRequest("Invalid email address")

    clean_email = validated_email.normalized.lower()
    name = validated_email.local_part.lower()[:80]

    user = User.query.filter_by(email=clean_email).first()
    if user:
        raise Conflict("User already exists")

    try:
        hashed_password = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        access_token = generate_jwt_token(user)
        data = {'access_token': access_token}

        return success_response(data=data, message="User successfully registered", status=201)

    except Exception as e:
        logging.error(e)
        raise InternalServerError("Error occurred, user registration failed")


@auth_bp.route("/session")
@jwt_required()
def session():
    data = {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
    }
    return success_response(data=data, message=f"Logged in as {current_user.name}")


@auth_bp.route("/logout", methods=['POST'])
@jwt_required()
def logout():
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    now = datetime.utcnow()
    db.session.add(TokenBlocklist(jti=jti, type=ttype, created_at=now))
    db.session.commit()

    return success_response(message=f"Logged out successfully")
