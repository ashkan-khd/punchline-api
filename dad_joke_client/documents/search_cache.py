from datetime import datetime, timezone, timedelta
from typing import List

from beanie import Document, Indexed


class SearchCache(Document):
    term: Indexed(str, unique=True)
    results: List[dict]
    last_access: Indexed(datetime, expireAfterSeconds=60) = datetime.now(timezone.utc)

    class Settings:
        collection = "search_cache"