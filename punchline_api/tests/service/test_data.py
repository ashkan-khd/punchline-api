import json
from pathlib import Path
from typing import List, Type

import pytest
from pydantic import BaseModel

from app.service import ServiceData, ServiceError
from app.service.chuck_norris import ChuckNorrisJoke
from app.service.dad_joke import DadJoke
from app.service.joke import ServiceJoke

@pytest.fixture
def _jsons_dir():
    current_dir = Path(__file__).parent
    return current_dir / "jsons"

@pytest.fixture
def mocked_list_chuck_norris_jokes(_jsons_dir):
    json_path = _jsons_dir / "list_chuck_norris_jokes.json"
    with json_path.open() as f:
        return json.load(f)

@pytest.fixture
def mocked_list_dad_jokes(_jsons_dir):
    json_path = _jsons_dir / "list_dad_jokes.json"
    with json_path.open() as f:
        return json.load(f)


@pytest.fixture
def mocked_chuck_norris_joke(_jsons_dir):
    json_path = _jsons_dir / "chuck_norris_joke.json"
    with json_path.open() as f:
        return json.load(f)


@pytest.fixture
def mocked_dad_joke(_jsons_dir):
    json_path = _jsons_dir / "dad_joke.json"
    with json_path.open() as f:
        return json.load(f)


class TestServiceData:
    @pytest.fixture(autouse=True)
    def setup(
            self,
            mocked_list_chuck_norris_jokes,
            mocked_list_dad_jokes,
            mocked_chuck_norris_joke,
            mocked_dad_joke,
    ):
        self.mocked_list_chuck_norris_jokes: List[dict] = mocked_list_chuck_norris_jokes
        self.mocked_list_dad_jokes: List[dict] = mocked_list_dad_jokes
        self.mocked_chuck_norris_joke: dict = mocked_chuck_norris_joke
        self.mocked_dad_joke: dict = mocked_dad_joke

    def _test_mocked_list_jokes(
            self,
            mocked_list_jokes: List[dict],
            actual_type: Type[BaseModel],
            field_dict: dict,
    ):
        service_data = ServiceData.model_validate(dict(successful=True, data=mocked_list_jokes))
        result_data = service_data.data

        assert isinstance(service_data.data_, list)
        assert isinstance(service_data.data_[0], actual_type)
        assert isinstance(result_data, list)
        assert isinstance(result_data[0], ServiceJoke)
        for i, service_joke in enumerate(result_data):
            assert service_joke.id == getattr(service_data.data_[i], field_dict["id"]) == \
                   mocked_list_jokes[i][field_dict["id"]]
            assert service_joke.value == getattr(service_data.data_[i], field_dict["value"]) == \
                   mocked_list_jokes[i][field_dict["value"]]

    def test_mocked_list_chuck_norris_jokes(self):
        self._test_mocked_list_jokes(
            self.mocked_list_chuck_norris_jokes,
            ChuckNorrisJoke,
            dict(id="id", value="value")
        )

    def test_mocked_list_dad_jokes(self):
        self._test_mocked_list_jokes(
            self.mocked_list_dad_jokes,
            DadJoke,
            dict(id="id", value="joke")
        )

    def _test_mocked_joke(
            self,
            mocked_joke: dict,
            actual_type: Type[BaseModel],
            field_dict: dict,
    ):
        service_data = ServiceData.model_validate(dict(successful=True, data=mocked_joke))
        result_data = service_data.data

        assert isinstance(service_data.data_, actual_type)
        assert isinstance(result_data, ServiceJoke)
        assert result_data.id == getattr(service_data.data_, field_dict["id"]) == mocked_joke[field_dict["id"]]
        assert result_data.value == getattr(service_data.data_, field_dict["value"]) == mocked_joke[field_dict["value"]]

    def test_mocked_chuck_norris_joke(self):
        self._test_mocked_joke(
            self.mocked_chuck_norris_joke,
            ChuckNorrisJoke,
            dict(id="id", value="value")
        )

    def test_mocked_dad_joke(self):
        self._test_mocked_joke(
            self.mocked_dad_joke,
            DadJoke,
            dict(id="id", value="joke")
        )

    def test_mocked_error(self):
        error = dict(error="ERROR", message="Error message")
        service_data = ServiceData.model_validate(dict(successful=False, data=error))
        result_data = service_data.data

        assert isinstance(service_data.data_, ServiceError)
        assert isinstance(result_data, ServiceError)
        assert result_data == service_data.data_
