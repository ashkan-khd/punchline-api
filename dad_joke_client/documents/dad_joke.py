from beanie import Document, Indexed
from typing import Dict


class DadJoke(Document):
    id: str
    joke: Dict

    class Settings:
        collection = "dad_jokes"