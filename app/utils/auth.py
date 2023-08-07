# Flask modules
from flask_jwt_extended import create_access_token

# Other modules
import uuid


def generate_jwt_token(user, additional_claims: dict = None):
    if additional_claims is None:
        additional_claims = dict()

    token_version = {"version": user.token_version}
    additional_claims.update(token_version)

    token = create_access_token(identity=user, additional_claims=additional_claims)
    return token


def shorten_uuid(input_uuid: uuid.UUID, length: int = 24):
    # Convert UUID to a hexadecimal string
    str_uuid = str(input_uuid)
    hex_uuid = str_uuid.replace('-', '')

    # Truncate to the desired length
    truncated_hex = hex_uuid[:length]

    return truncated_hex


def generate_uuid(length: int = None):
    if length:
        return shorten_uuid(uuid.uuid4())

    return str(uuid.uuid4())
