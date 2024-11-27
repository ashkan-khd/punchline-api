import pytest
from nameko.testing.services import worker_factory
from service import ChuckNorrisService, ChuckNorrisServiceData
from client import ChuckNorrisClientException


@pytest.fixture
def service():
    return worker_factory(ChuckNorrisService)


@pytest.fixture
def mock_client_property(mocker):
    return mocker.patch.object(ChuckNorrisService, 'client', new_callable=mocker.PropertyMock)


class TestChuckNorrisService:

    @pytest.fixture(autouse=True)
    def setup(self, service, mock_client_property):
        self.service = service
        self.mock_client = mock_client_property.return_value

    def test_query_jokes_success(self):
        self.mock_client.get_joke_by_search.return_value = {"joke": "Funny joke"}
        q = "funny"

        result = self.service.query_jokes(q)

        expected = ChuckNorrisServiceData(successful=True, data={"joke": "Funny joke"}).to_dict()
        assert result == expected
        self.mock_client.get_joke_by_search.assert_called_once_with(q)

    def test_query_jokes_failure(self):
        mock_exception = ChuckNorrisClientException("ERR", "Not found")
        self.mock_client.get_joke_by_search.side_effect = mock_exception

        result = self.service.query_jokes("unknown")

        expected = ChuckNorrisServiceData(successful=False, data={"error": "ERR", "message": "Not found"}).to_dict()
        assert result == expected

    def test_get_joke_success(self):
        self.mock_client.get_joke_by_id.return_value = {"joke": "Specific joke"}

        result = self.service.get_joke("123")

        expected = ChuckNorrisServiceData(successful=True, data={"joke": "Specific joke"}).to_dict()
        assert result == expected

    def test_get_joke_failure(self):
        mock_exception = ChuckNorrisClientException("ERR", "Not found")
        self.mock_client.get_joke_by_id.side_effect = mock_exception

        result = self.service.get_joke("unknown")

        expected = ChuckNorrisServiceData(successful=False, data={"joke": "Specific joke"}).to_dict()
        assert result == expected
