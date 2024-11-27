import dataclasses

from nameko.rpc import rpc
from punchline_interfaces import ChuckNorrisServiceInterface

import client


@dataclasses.dataclass
class ChuckNorrisServiceData:
    successful: bool
    data: dict

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)


class ChuckNorrisService(ChuckNorrisServiceInterface):

    @property
    def client(self) -> client.ChuckNorrisClientInterface:
        return client.get_chuck_norris_client()

    @rpc
    def query_jokes(self, query: str) -> dict:
        try:
            result = self.client.get_joke_by_search(query)
            successful = True
        except client.ChuckNorrisClientException as e:
            result = e.to_dict()
            successful = False
        return ChuckNorrisServiceData(successful=successful, data=result).to_dict()

    @rpc
    def get_joke(self, joke_id: str) -> dict:
        try:
            result = self.client.get_joke_by_id(joke_id)
            successful = True
        except client.ChuckNorrisClientException as e:
            result = e.to_dict()
            successful = False
        return ChuckNorrisServiceData(successful=successful, data=result).to_dict()
