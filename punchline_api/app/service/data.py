from functools import cached_property
from typing import Union, List, Any, Optional

from pydantic import BaseModel

from .converter import ServiceJokeConverter
from .chuck_norris import ChuckNorrisJoke
from .dad_joke import DadJoke

from .error import ServiceError
from .joke import ServiceJoke

ServiceDataType = Union[ServiceError, ServiceJoke, List[ServiceJoke]]


class ServiceData(BaseModel):
    successful: bool
    data_: Union[ServiceError, Union[DadJoke, ChuckNorrisJoke], List[Union[DadJoke, ChuckNorrisJoke]]]

    def __init__(self, /, **data: Any):
        if "data" in data:
            data["data_"] = data["data"]
        super().__init__(**data)
        self.__cleaned_data: Optional[ServiceDataType] = None

    @property
    def data(self) -> ServiceDataType:
        if self.__cleaned_data is None:
            self.__cleaned_data = self.__convert_data_type()
        return self.__cleaned_data

    @cached_property
    def __converter(self) -> ServiceJokeConverter:
        return ServiceJokeConverter()

    def __convert_data_type(
            self,
    ) -> ServiceDataType:
        if isinstance(self.data_, ServiceError):
            return self.data_
        joke: Union["DadJoke", "ChuckNorrisJoke"]
        if isinstance(self.data_, list):
            return [joke.accept_converter(self.__converter) for joke in self.data_]
        else:
            joke = self.data_
            return joke.accept_converter(self.__converter)
