from pydantic import BaseModel


class ServiceError(BaseModel):
    error: str = None
    message: str = None

