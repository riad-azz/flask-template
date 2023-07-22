from dataclasses import dataclass
from app.utils.models import SerializableDataclass


@dataclass
class TestModel(SerializableDataclass):
    title: str
    content: str
