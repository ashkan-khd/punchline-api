from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.models import JokeValueFields


class ServiceJoke(BaseModel, JokeValueFields):
    categories: List[str] = Field(default_factory=list)
    created_at: datetime = None
    updated_at: datetime = None
    local: bool = False