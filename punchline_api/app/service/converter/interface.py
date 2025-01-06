from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from app.service.chuck_norris import ChuckNorrisJoke
    from app.service.dad_joke import DadJoke


class JokeConverterInterface(ABC):

    @abstractmethod
    def convert_chuck_norris_joke(self, joke: "ChuckNorrisJoke") -> BaseModel:
        ...

    @abstractmethod
    def convert_dad_joke(self, joke: "DadJoke") -> BaseModel:
        ...
