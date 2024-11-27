from typing import Dict

import requests
from requests import Response

from interface import implements

from .interface import ChuckNorrisClientInterface, ChuckNorrisClientException


class ChuckNorrisClient(implements(ChuckNorrisClientInterface)):
    BASE_URL = "https://api.chucknorris.io/jokes"

    def get_joke_by_search(self, query: str) -> Dict:
        response: Response = requests.get(
            f"{self.BASE_URL}/search", params={"query": query}
        )
        if response.status_code != 200:
            raise ChuckNorrisClientException(
                error="QUERY_ERROR",
                message=f"Failed to fetch jokes with status code: {response.status_code} and message: {response.text}",
            )
        return response.json().get("result", [])

    def get_joke_by_id(self, id_: str) -> Dict:
        response: Response = requests.get(f"{self.BASE_URL}/{id_}")
        if response.status_code != 200:
            raise ChuckNorrisClientException(
                error="ID_ERROR",
                message=f"Failed to fetch joke with id: {id_} with status code: {response.status_code} and message: {response.text}",
            )
        return response.json()
