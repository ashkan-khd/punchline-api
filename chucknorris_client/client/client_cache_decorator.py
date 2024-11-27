import json
from typing import Dict

from interface import implements
from redis import StrictRedis

from .interface import ChuckNorrisClientInterface


class ChuckNorrisClientCacheDecorator(implements(ChuckNorrisClientInterface)):

    def __init__(self, client: ChuckNorrisClientInterface, cache: StrictRedis):
        self.client = client
        self.cache: StrictRedis = cache

    def get_joke_by_search(self, query: str) -> Dict:
        if self.cache.exists(query):
            print("hit the cache for search")
            return json.loads(self.cache.get(query))
        result = self.client.get_joke_by_search(query)
        self.cache.set(query, json.dumps(result), ex=5 * 60)
        return result

    def get_joke_by_id(self, id_: str) -> Dict:
        if self.cache.exists(id_):
            print("hit the cache for id")
            return json.loads(self.cache.get(id_))
        result = self.client.get_joke_by_id(id_)
        self.cache.set(id_, json.dumps(result), ex=60 * 60)
        return result
