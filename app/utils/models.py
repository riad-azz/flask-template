# Other modules
import json
import uuid


class SerializableClass:
    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def is_serializable(obj):
        try:
            json.dumps(obj)
            return True
        except:
            return False


def shorten_uuid(input_uuid: uuid.UUID, length: int = 24) -> str:
    # Convert UUID to a hexadecimal string
    str_uuid = str(input_uuid)
    hex_uuid = str_uuid.replace("-", "")

    # Truncate to the desired length
    truncated_hex = hex_uuid[:length]

    return truncated_hex


def generate_uuid(length: int = None) -> str:
    if length:
        return shorten_uuid(uuid.uuid4())

    str_uuid = str(uuid.uuid4())
    return str_uuid
