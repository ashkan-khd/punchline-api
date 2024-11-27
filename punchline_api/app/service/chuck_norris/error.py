from pydantic import BaseModel


class ChuckNorrisErrorData(BaseModel):
    error: str
    message: str

