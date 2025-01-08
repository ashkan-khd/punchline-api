import asyncio
from datetime import datetime, timezone
from typing import Dict, List

import httpx
from pymongo.errors import DuplicateKeyError

from documents import SearchCache, DadJoke


# logger = logging.getLogger(__name__)

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

    async def _update_search_cache(self, term: str, results: List[Dict]) -> None:
        if not results:
            return

        search_cache = await SearchCache.find_one(SearchCache.term == term)

        if search_cache:
            await search_cache.set({SearchCache.results: search_cache.results + results})
            await search_cache.set({SearchCache.last_access: datetime.now(timezone.utc)})


    async def _get_joke_by_search_for_page_and_update(self, term: str, page: int, update: bool) -> List[Dict]:
        response_json = await self._get_joke_by_search_for_page(term, page)
        results = response_json["results"]
        if update:
            await self._update_search_cache(term, results)
        return results

    async def _create_search_cache(self, term: str, results: List[Dict]) -> bool:
        created = True
        try:
            await SearchCache(term=term, results=results).insert()
        except DuplicateKeyError:
            created = False
        return created

    async def _get_joke_from_cache(self, term: str) -> List[Dict]:
        search_cache = await SearchCache.find_one(SearchCache.term == term)
        if search_cache:
            await search_cache.set({SearchCache.last_access: datetime.now(timezone.utc)})
            return search_cache.results
        return []

    async def get_joke_by_search(self, term: str) -> List[Dict]:
        if cached_result := await self._get_joke_from_cache(term):
            return cached_result

        first_page_response = await self._get_joke_by_search_for_page(term, 1)
        results = first_page_response["results"]
        created = await self._create_search_cache(term, results)

        tasks = [
            self._get_joke_by_search_for_page_and_update(term, page, created)
            for page in range(2, first_page_response["total_pages"] + 1)
        ]
        other_pages = await asyncio.gather(*tasks, return_exceptions=True)

        for page in other_pages:
            if isinstance(page, Exception):
                continue
            results.extend(page)

        return results

    async def get_joke_by_id(self, id_: str) -> Dict:
        dad_joke = await DadJoke.find_one(DadJoke.id == id_)
        if dad_joke:
            return dad_joke.joke

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/j/{id_}",
                headers=self.BASE_HEADERS,
            )
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch joke with id: {id_} with status code: {response.status_code} and message: {response.text}"
            )
        joke = response.json()

        await DadJoke(id=id_, joke=joke).insert()

        return joke
