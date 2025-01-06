from app.service import ServiceJoke
from app.service.chuck_norris import ChuckNorrisJoke
from app.service.dad_joke import DadJoke

from .interface import JokeConverterInterface


class ServiceJokeConverter(JokeConverterInterface):

    def convert_chuck_norris_joke(self, joke: ChuckNorrisJoke) -> ServiceJoke:
        return ServiceJoke(
            id=joke.id,
            value=joke.value,
            categories=joke.categories,
            created_at=joke.created_at,
            updated_at=joke.updated_at,
        )

    def convert_dad_joke(self, joke: DadJoke) -> ServiceJoke:
        return ServiceJoke(
            id=joke.id,
            value=joke.joke,
        )
