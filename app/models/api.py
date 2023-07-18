from app.utils.models import JSONSerializable


class APIResponse(JSONSerializable):
    def __init__(self, status: str):
        self.status = status


class SuccessResponse(APIResponse):
    def __init__(self, data):
        super().__init__(status="success")
        self.data = data


class ErrorResponse(APIResponse):
    def __init__(self, message):
        super().__init__(status="error")
        self.message = message
