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
from app.extensions import db, limiter
from app.utils.api import success_response
from app.utils.auth import generate_jwt_token
from app.models.auth import User, TokenBlocklist

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=['POST'])
@limiter.limit("5/minute")
def login():
    """
    Logs in a user by validating their email and password, generating an access token, and returning a success response.

    Returns:
        A success response containing the access token and a message indicating successful login.

    Raises:
        BadRequest: If the email or password is missing, the email address is invalid, the user does not exist, or the credentials are invalid.
    """
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
@limiter.limit("10/minute")
def register():
    """
    Register a new user.
    This function handles the registration of a new user. 
    It expects a JSON payload containing the user's email and password. 

    Returns:
        A success response containing the access token and a message.

    Raises:
        BadRequest: If the email address or password is missing, or if the email address is invalid.
        Conflict: If a user with the same email address already exists.
        InternalServerError: If an error occurs during the registration process.
    """
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
    """
    Retrieves the session information for the authenticated user.

    Returns:
        dict: A dictionary containing the session information. The dictionary has the following keys:
            - id (int): The ID of the user.
            - name (str): The name of the user.
            - email (str): The email address of the user.

    Raises:
        jwt.exceptions.InvalidTokenError: If the JWT token is invalid or expired.
    """
    data = {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
    }
    return success_response(data=data, message=f"Logged in as {current_user.name}")


@auth_bp.route("/logout", methods=['POST'])
@jwt_required()
def logout():
    """
    Logs out the user by adding the JWT token to the token blocklist.

    Returns:
        A success response message indicating that the user has been logged out successfully.
    """
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    now = datetime.utcnow()
    db.session.add(TokenBlocklist(jti=jti, type=ttype, created_at=now))
    db.session.commit()

    return success_response(message=f"Logged out successfully")
