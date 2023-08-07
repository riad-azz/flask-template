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

    def __init__(self, status: str, message: str, data=None):
        self.status = status
        self.message = message
        self.data = data

    def to_dict(self):
        response_dict = dict()
        response_dict["status"] = self.status

        if self.message:
            response_dict["message"] = self.message

        if self.data:
            response_dict["data"] = self.data

        return response_dict


class SuccessResponse(APIResponse):
    def __init__(self, data=None, message: str = ""):
        super().__init__(status="success", message=message, data=data)


class ErrorResponse(APIResponse):
    def __init__(self, message: str = None):
        if message is None:
            message = "Internal Server Error"
        super().__init__(status="error", message=message)
