# Other modules
import uuid


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
