import pytest

from app.models import Joke


class TestListCreateJokeResource:
    @pytest.fixture(autouse=True)
    def setup(self, client, mocked_chuck_norris_service, mocked_dad_joke_service, joke):
        self.client = client
        self.mocked_chuck_norris_service = mocked_chuck_norris_service
        self.mocked_dad_joke_service = mocked_dad_joke_service
        self.joke = joke

    def test_list_jokes(self):
        chucknorris_id = "Bup36JbASxW5R-HzSI5ygA"
        self.mocked_chuck_norris_service.return_value.query_jokes.return_value = dict(
            successful=True,
            data=[
                {
                    'categories': [],
                    'created_at': '2020-01-05 13:42:19.897976',
                    'icon_url': 'https://api.chucknorris.io/img/avatar/chuck-norris.png',
                    'id': chucknorris_id,
                    'updated_at': '2020-01-05 13:42:19.897976',
                    'url': 'https://api.chucknorris.io/jokes/Bup36JbASxW5R-HzSI5ygA',
                    'value': 'Chuck Norris once participated in a 100 mt race and obviously came first, '
                             'but Albert Einstein died after watching that cos light came second.',
                }
            ]
        )
        self.mocked_dad_joke_service.return_value.query_jokes.return_value = dict(
            successful=False,
            data=dict(
                error="QUERY_ERROR",
                message="Failed to fetch jokes with status code: 404 and message: Not Found",
            ),
        )

        response = self.client.get("/api/jokes/?query=divide")
        assert response.status_code == 200
        assert {joke["id"] for joke in response.json} == {chucknorris_id, str(self.joke.id)}
        self.mocked_chuck_norris_service.return_value.query_jokes.assert_called_once_with("divide")

    def test_create_joke(self):
        response = self.client.post("/api/jokes/", json={"value": "New joke", "categories": ["nerdy"]})
        assert response.status_code == 201
        assert response.json["value"] == "New joke"
        assert response.json["categories"] == ["nerdy"]
        assert Joke.query.filter_by(value="New joke").first() is not None