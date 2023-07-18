import json
from dataclasses_serialization.json import JSONSerializer


class JSONSerializable:
    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()

    def to_dict(self):
        return self.__dict__


class APIResponse(JSONSerializable):
    def __init__(self, status: str):
        self.status = status


class SuccessResponse(APIResponse):
    def __init__(self, data):
        super().__init__(status="success")
        self.data = JSONSerializer.serialize(data)


class ErrorResponse(APIResponse):
    def __init__(self, message):
        super().__init__(status="error")
        self.message = message
