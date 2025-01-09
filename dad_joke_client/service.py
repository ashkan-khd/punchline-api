import asyncio
import dataclasses
import logging

from nameko.rpc import rpc
from punchline_interfaces import DadJokeServiceInterface

from client import DadJokeClient
from dependencies import BeanieDatabaseProvider

# logger = logging.getLogger(__name__)


@dataclasses.dataclass
class DadJokeServiceData:
    successful: bool
    data: dict

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)


class DadJokeService(DadJokeServiceInterface):
    loop = BeanieDatabaseProvider(db_uri="mongodb://mongo:27017", db_name="dadjokes")  # Configure as needed

    @property
    def client(self) -> DadJokeClient:
        return DadJokeClient()

    @rpc
    def query_jokes(self, query: str) -> dict:
        try:
            result = self.loop.run_until_complete(self.client.get_joke_by_search(query))
            successful = True
        except Exception as e:
            result = {"message": str(e)}
            successful = False
        return DadJokeServiceData(successful=successful, data=result).to_dict()

    @rpc
    def get_joke(self, joke_id: str) -> dict:
        try:
            result = self.loop.run_until_complete(self.client.get_joke_by_id(joke_id))
            successful = True
        except Exception as e:
            result = {"message": str(e)}
            successful = False
        return DadJokeServiceData(successful=successful, data=result).to_dict()
