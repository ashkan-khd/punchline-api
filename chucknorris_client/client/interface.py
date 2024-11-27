from typing import Dict, Optional

from redis import StrictRedis
from requests import Response

from interface import Interface


class ChuckNorrisClientException(Exception):
    error: str
    message: str

    def __init__(self, error, message):
        super().__init__(message)
        self.error = error
        self.message = message

    def to_dict(self) -> Dict:
        return {
            "error": self.error,
            "message": self.message
        }


class ChuckNorrisClientInterface(Interface):

    def get_joke_by_search(self, query: str) -> Dict:
        pass

    def get_joke_by_id(self, id_: str) -> Dict:
        pass


def get_chuck_norris_client(cache: Optional[StrictRedis] = None) -> ChuckNorrisClientInterface:
    from .concrete_client import ChuckNorrisClient
    from .client_cache_decorator import ChuckNorrisClientCacheDecorator
    client = ChuckNorrisClient()
    if cache is not None:
        client = ChuckNorrisClientCacheDecorator(client, cache)
    return client
