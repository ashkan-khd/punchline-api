import pytest

from app.models import Joke


class TestRetrieveUpdateDeleteJokeResource:
    @pytest.fixture(autouse=True)
    def setup(self, client, mocked_service, joke):
        self.client = client
        self.mocked_service = mocked_service
        self.joke = joke

    def test_retrieve_joke_locally(self):
        response = self.client.get(f"/api/jokes/{self.joke.id}/")
        assert response.status_code == 200
        assert response.json["id"] == str(self.joke.id)

    def test_retrieve_joke_externally(self):
        chucknorris_id = "Bup36JbASxW5R-HzSI5ygA"
        self.mocked_service.return_value.get_joke.return_value = dict(
            successful=True,
            data={
                'categories': [],
                'created_at': '2020-01-05 13:42:19.897976',
                'icon_url': 'https://api.chucknorris.io/img/avatar/chuck-norris.png',
                'id': chucknorris_id,
                'updated_at': '2020-01-05 13:42:19.897976',
                'url': 'https://api.chucknorris.io/jokes/Bup36JbASxW5R-HzSI5ygA',
                'value': 'Chuck Norris once participated in a 100 mt race and obviously came first, '
                         'but Albert Einstein died after watching that cos light came second.',
            }
        )
        response = self.client.get(f"/api/jokes/{chucknorris_id}/")
        assert response.status_code == 200
        assert response.json["id"] == chucknorris_id
        self.mocked_service.return_value.get_joke.assert_called_once_with(chucknorris_id)


    def test_retrieve_joke_not_found(self):
        self.mocked_service.return_value.get_joke.return_value = dict(
            successful=False,
            data={
                "error": "ID_ERROR",
                "message": "Failed to fetch joke with id: 2 with status code: 404 and message: Not Found",
            },
        )
        response = self.client.get(f"/api/jokes/2/")
        assert response.status_code == 404

    def test_update_joke(self):
        response = self.client.put(f"/api/jokes/{self.joke.id}/", json={"value": "Updated joke", "categories": ["nerdy"]})
        assert response.status_code == 200
        assert response.json["value"] == "Updated joke"
        assert response.json["categories"] == ["nerdy"]

    def test_delete_joke(self):
        response = self.client.delete(f"/api/jokes/{self.joke.id}/")
        assert response.status_code == 204
        assert Joke.query.get(self.joke.id).is_deleted
