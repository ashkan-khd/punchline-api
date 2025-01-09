from abc import ABC

from punchline_interfaces import ServiceInterface


class BaseJokeClientServiceInterface(ServiceInterface, ABC):

    def query_jokes(self, query: str) -> dict:
        raise NotImplementedError

    def get_joke(self, joke_id: str) -> dict:
        raise NotImplementedError