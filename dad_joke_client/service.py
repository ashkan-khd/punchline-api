import asyncio
import dataclasses

from nameko.rpc import rpc
from punchline_interfaces import DadJokeServiceInterface

from client import DadJokeClient


@dataclasses.dataclass
class DadJokeServiceData:
    successful: bool
    data: dict

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)


class DadJokeService(DadJokeServiceInterface):

    @property
    def client(self) -> DadJokeClient:
        return DadJokeClient()

    @rpc
    def query_jokes(self, query: str) -> dict:
        try:
            result = asyncio.run(self.client.get_joke_by_search(query))
            successful = True
        except Exception as e:
            result = {"message": str(e)}
            successful = False
        return DadJokeServiceData(successful=successful, data=result).to_dict()

    @rpc
    def get_joke(self, joke_id: str) -> dict:
        try:
            result = asyncio.run(self.client.get_joke_by_id(joke_id))
            successful = True
        except Exception as e:
            result = {"message": str(e)}
            successful = False
        return DadJokeServiceData(successful=successful, data=result).to_dict()
