from dataclasses import dataclass
from app.utils.models import SerializableDataclass


@dataclass
class ExampleModel(SerializableDataclass):
    title: str
    content: str
