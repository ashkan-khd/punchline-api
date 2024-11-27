from punchline_interfaces.service_interface import ServiceInterface


class ChuckNorrisServiceInterface(ServiceInterface):
    name = "chuck_norris"

    def query_jokes(self, query: str) -> dict:
        raise NotImplementedError

    def get_joke(self, joke_id: str) -> dict:
        raise NotImplementedError
