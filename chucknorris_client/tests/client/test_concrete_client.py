import pytest
import requests_mock

from client.interface import ChuckNorrisClientException


@pytest.fixture
def client():
    from client.concrete_client import ChuckNorrisClient
    return ChuckNorrisClient()


class TestChuckNorrisClient:

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client

    def test_get_joke_by_search_success(self):
        query = "funny"
        with requests_mock.Mocker() as m:
            m.get(f"https://api.chucknorris.io/jokes/search?query={query}",
                  json={"result": [{"id": "123", "value": "A funny joke"}]})
            result = self.client.get_joke_by_search(query)
            assert result == [{"id": "123", "value": "A funny joke"}]

    def test_get_joke_by_search_failure(self):
        query = "funny"
        with requests_mock.Mocker() as m:
            m.get(f"https://api.chucknorris.io/jokes/search?query={query}", status_code=404, text="Not Found")
            with pytest.raises(ChuckNorrisClientException):
                self.client.get_joke_by_search(query)

    def test_get_joke_by_id_success(self):
        joke_id = "123"
        with requests_mock.Mocker() as m:
            m.get(f"https://api.chucknorris.io/jokes/{joke_id}", json={"id": "123", "value": "A funny joke"})
            result = self.client.get_joke_by_id(joke_id)
            assert result == {"id": "123", "value": "A funny joke"}

    def test_get_joke_by_id_failure(self):
        joke_id = "123"
        with requests_mock.Mocker() as m:
            m.get(f"https://api.chucknorris.io/jokes/{joke_id}", status_code=404, text="Not Found")
            with pytest.raises(ChuckNorrisClientException):
                self.client.get_joke_by_id(joke_id)
