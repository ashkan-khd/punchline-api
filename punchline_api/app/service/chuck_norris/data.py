from typing import Union, List

from pydantic import BaseModel

from .error import ChuckNorrisErrorData
from .joke import ChuckNorrisJoke


class ChuckNorrisServiceData(BaseModel):
    successful: bool
    data: Union[ChuckNorrisErrorData, ChuckNorrisJoke, List[ChuckNorrisJoke]]
