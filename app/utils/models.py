import json


class SerializableClass:
    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def is_json_serializable(obj):
        try:
            json.dumps(obj)
            return True
        except:
            return False


class APIResponse(SerializableClass):

    def __init__(self, status: str, data: dict):
        self.status = status
        self.data = data

    def to_dict(self):
        response_dict = {"status": self.status}
        response_dict.update(self.data)
        return response_dict


class SuccessResponse(APIResponse):
    def __init__(self, data: dict):
        super().__init__(status="success", data=data)


class ErrorResponse(APIResponse):
    def __init__(self, data: dict):
        super().__init__(status="error", data=data)
