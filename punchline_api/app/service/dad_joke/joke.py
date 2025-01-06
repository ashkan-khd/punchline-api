from pydantic import BaseModel
from app.service.converter import JokeConverterInterface


class DadJoke(BaseModel):
    id: str
    joke: str

    class Config:
        # Allow population by field name
        populate_by_alias = True

        # Configure how the model should handle extra fields
        extra = "ignore"

    def accept_converter(self, converter: JokeConverterInterface):
        return converter.convert_dad_joke(self)
