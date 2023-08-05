from pydantic import BaseModel


class TestModel(BaseModel):
    title: str
    content: str
