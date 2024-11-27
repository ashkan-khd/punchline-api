from typing import List

from pydantic import BaseModel, field_validator
from datetime import datetime


class ChuckNorrisJoke(BaseModel):
    id: str
    categories: List[str]
    created_at: datetime
    updated_at: datetime
    value: str
    local: bool = False

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S.%f")
        }

        # Allow population by field name
        populate_by_alias = True

        # Configure how the model should handle extra fields
        extra = "ignore"

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        # Convert string datetime fields to datetime objects if they're strings
        if isinstance(obj.get("created_at"), str):
            obj["created_at"] = datetime.strptime(obj["created_at"], "%Y-%m-%d %H:%M:%S.%f")
        if isinstance(obj.get("updated_at"), str):
            obj["updated_at"] = datetime.strptime(obj["updated_at"], "%Y-%m-%d %H:%M:%S.%f")
        return super().model_validate(obj, *args, **kwargs)