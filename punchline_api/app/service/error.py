from pydantic import BaseModel


class ServiceError(BaseModel):
    error: str
    message: str

