from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar("T")

class Response(BaseModel, Generic[T]):
    data: T
    status: int
    headers: dict
    response_time: int
