import json
from unittest.mock import MagicMock

import pytest
import requests_mock


@pytest.fixture
def client():
    from client.concrete_client import ChuckNorrisClient
    return ChuckNorrisClient()


@pytest.fixture
def cache():
    return MagicMock()


@pytest.fixture
def cached_client(client, cache):
    from client.client_cache_decorator import ChuckNorrisClientCacheDecorator
    return ChuckNorrisClientCacheDecorator(client, cache)


class TestChuckNorrisClientCacheDecorator:

    @pytest.fixture(autouse=True)
    def setup(self, cached_client, cache):
        self.cached_client = cached_client
        self.cache = cache

    def test_get_joke_by_search_cache_hit(self):
        query = "funny"
        self.cache.exists.return_value = True
        self.cache.get.return_value = json.dumps([{"id": "123", "value": "A funny joke"}])

        result = self.cached_client.get_joke_by_search(query)

        self.cache.exists.assert_called_once_with(query)
        self.cache.get.assert_called_once_with(query)
        assert result == [{"id": "123", "value": "A funny joke"}]

    def test_get_joke_by_search_cache_miss(self):
        query = "funny"
        self.cache.exists.return_value = False
        with requests_mock.Mocker() as m:
            m.get(f"https://api.chucknorris.io/jokes/search?query={query}",
                  json={"result": [{"id": "123", "value": "A funny joke"}]})

            result = self.cached_client.get_joke_by_search(query)

            self.cache.exists.assert_called_once_with(query)
            self.cache.set.assert_called_once_with(query, json.dumps([{"id": "123", "value": "A funny joke"}]),
                                                   ex=5 * 60)
            assert result == [{"id": "123", "value": "A funny joke"}]

    def test_get_joke_by_id_cache_hit(self):
        joke_id = "123"
        self.cache.exists.return_value = True
        self.cache.get.return_value = json.dumps({"id": "123", "value": "A funny joke"})

        result = self.cached_client.get_joke_by_id(joke_id)

        self.cache.exists.assert_called_once_with(joke_id)
        self.cache.get.assert_called_once_with(joke_id)
        assert result == {"id": "123", "value": "A funny joke"}

    def test_get_joke_by_id_cache_miss(self):
        joke_id = "123"
        self.cache.exists.return_value = False
        with requests_mock.Mocker() as m:
            m.get(f"https://api.chucknorris.io/jokes/{joke_id}", json={"id": "123", "value": "A funny joke"})

            result = self.cached_client.get_joke_by_id(joke_id)

            self.cache.exists.assert_called_once_with(joke_id)
            self.cache.set.assert_called_once_with(joke_id, json.dumps({"id": "123", "value": "A funny joke"}),
                                                   ex=60 * 60)
            assert result == {"id": "123", "value": "A funny joke"}
