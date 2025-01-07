import asyncio
from typing import Dict, List

import httpx


class DadJokeClient:
    BASE_URL = "https://icanhazdadjoke.com"
    BASE_HEADERS = {"Accept": "application/json"}

    async def _get_joke_by_search_for_page(self, term: str, page: int) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/search",
                headers=self.BASE_HEADERS,
                params={"term": term, "limit": 30, page: page}
            )
            if response.status_code != 200:
                raise Exception(
                    f"Failed to fetch jokes with status code: {response.status_code} and message: {response.text}"
                )
            return response.json()

    async def get_joke_by_search(self, term: str) -> List[Dict]:
        first_page = await self._get_joke_by_search_for_page(term, 1)
        tasks = [
            self._get_joke_by_search_for_page(term, page)
            for page in range(2, first_page["total_pages"])
        ]
        other_pages = await asyncio.gather(*tasks, return_exceptions=True)
        result = [
            *first_page["results"],
        ]
        for page in other_pages:
            if isinstance(page, Exception):
                continue
            result.extend(page["results"])
        return result

    async def get_joke_by_id(self, id_: str) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/j/{id_}",
                headers=self.BASE_HEADERS,
            )
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch joke with id: {id_} with status code: {response.status_code} and message: {response.text}"
            )
        return response.json()
